#!/usr/bin/env python3
"""
Safely update ROCm sources in rocm.spec from a RHEL repo.
"""

from __future__ import annotations

import argparse
import bz2
import contextlib
import dataclasses
import logging
import os
import re
import shutil
import sqlite3
import string
import sys
import tempfile
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from typing import Optional, Tuple

# --- Defaults (configurable via CLI where it makes sense) ---
RHEL_DEFAULT = "8"
ARCH_DEFAULT = "x86_64"
URL_ROOT_DEFAULT = "https://repo.radeon.com/rocm/"
USER_AGENT = "rocm-updater/1.0 (+https://example.local)"

# Namespaces used in repodata
REPO_NS = {"repo": "http://linux.duke.edu/metadata/repo"}


# --- Exceptions ---------------------------------------------------------------

class RocmUpdateError(Exception):
    """Top-level domain error for update failures."""


class NetworkError(RocmUpdateError):
    pass


class XmlParseError(RocmUpdateError):
    pass


class RepoSchemaError(RocmUpdateError):
    pass


class DatabaseError(RocmUpdateError):
    pass


class SpecFileError(RocmUpdateError):
    pass


# --- Helpers -----------------------------------------------------------------

def make_url(url: str, url_root: str) -> str:
    if not isinstance(url, str):
        raise TypeError(f"URL must be a string, got: {type(url)}")
    u = url.lstrip("/")
    if u.startswith("http://") or u.startswith("https://"):
        return u
    return url_root.rstrip("/") + "/" + u


def fetch(
        url: str,
        *,
        timeout: float,
        retries: int,
        backoff_base: float = 0.5,
        url_root: str,
) -> bytes:
    """HTTP GET with retries/backoff and clear errors."""
    target = make_url(url, url_root)
    last_exc: Optional[BaseException] = None
    headers = {"User-Agent": USER_AGENT}

    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(target, headers=headers, method="GET")
            with contextlib.closing(urllib.request.urlopen(req, timeout=timeout)) as resp:
                code = getattr(resp, "status", resp.getcode())
                if code != 200:
                    raise NetworkError(f"GET {target} -> HTTP {code}")
                return resp.read()
        except urllib.error.HTTPError as e:
            # 4xx/5xx: retry only some statuses (e.g. 502/503/504)
            if e.code in (502, 503, 504):
                last_exc = e
            else:
                raise NetworkError(f"GET {target} failed: HTTP {e.code}") from e
        except urllib.error.URLError as e:
            # transient network failures may be retried
            last_exc = e
        except Exception as e:
            last_exc = e

        if attempt < retries:
            delay = backoff_base * (2 ** attempt)
            logging.warning("Fetch failed (attempt %d/%d): %s; retrying in %.1fs",
                            attempt + 1, retries + 1, last_exc, delay)
            time.sleep(delay)

    assert last_exc is not None
    raise NetworkError(f"GET {target} ultimately failed after {retries + 1} attempts") from last_exc


def fetch_repodata(version: str, *, rhel: str, url_root: str, timeout: float, retries: int) -> bytes:
    path = f"rhel{rhel}/{version}/main/repodata/repomd.xml"
    return fetch(path, timeout=timeout, retries=retries, url_root=url_root)


def fetch_db(version: str, url: str, *, rhel: str, url_root: str, timeout: float, retries: int) -> str:
    db_bz2 = fetch(f"rhel{rhel}/{version}/main/{url}", timeout=timeout, retries=retries, url_root=url_root)
    try:
        db_b = bz2.decompress(db_bz2)
    except OSError as e:
        raise DatabaseError("Failed to decompress primary_db .bz2") from e

    fd, db_path = tempfile.mkstemp(suffix=".db", prefix="rocm_primary_")
    with os.fdopen(fd, "wb") as fp:
        fp.write(db_b)
    return db_path


def parse_primary_db_href(repomd_xml: bytes) -> str:
    try:
        tree = ET.fromstring(repomd_xml)
    except ET.ParseError as e:
        raise XmlParseError("repomd.xml is not valid XML") from e

    node = tree.find("repo:data[@type='primary_db']/repo:location", REPO_NS)
    if node is None:
        raise RepoSchemaError("repomd.xml missing primary_db location")
    href = node.get("href")
    if not href:
        raise RepoSchemaError("primary_db location@href is empty/missing")
    return href.lstrip("/")


def compute_rpmvars(version: str, rhel: str, arch: str, url_root: str) -> dict[str, str]:
    """Return rpmvars as a plain dict, for easy string.Template substitution."""
    repoversion = re.sub(r"\.0$", "", version)
    repository = f"repo.radeon.com/rocm/rhel{rhel}"
    return {
        "rhel": rhel,
        "_arch": arch,
        "realversion": version,
        "repoversion": repoversion,
        "repository": repository,
    }


def open_sqlite(db_path: str) -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to open sqlite DB: {db_path}") from e


def read_rocm_spec(spec_path: str) -> list[str]:
    if not os.path.exists(spec_path):
        raise SpecFileError(f"Spec file not found: {spec_path}")
    try:
        with open(spec_path, "r", encoding="utf-8") as f:
            return f.readlines()
    except OSError as e:
        raise SpecFileError(f"Failed to read spec file: {spec_path}") from e


def atomic_write_with_backup(path: str, new_lines: list[str]) -> None:
    dirpath = os.path.dirname(path) or "."
    tmp_fd, tmp_path = tempfile.mkstemp(prefix="rocm_spec_", suffix=".tmp", dir=dirpath)
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8", newline="") as wf:
            wf.writelines(new_lines)
        # Backup only once per run; overwrite backup if it exists.
        backup_path = path + ".bak"
        try:
            shutil.copy2(path, backup_path)
        except Exception:
            # If the file doesn't exist yet, that's fine.
            pass
        os.replace(tmp_path, path)
    except Exception:
        # ensure temp file does not linger
        with contextlib.suppress(Exception):
            os.unlink(tmp_path)
        raise


def update_rocm(
        version: str,
        cmsdist_dir: str,
        *,
        rhel: str,
        arch: str,
        url_root: str,
        timeout: float,
        retries: int,
        dry_run: bool = False,
) -> Tuple[int, int]:
    """
    Returns: (num_sources_examined, num_sources_changed)
    """
    repodata_s = fetch_repodata(version, rhel=rhel, url_root=url_root, timeout=timeout, retries=retries)
    db_href = parse_primary_db_href(repodata_s)
    db_path = fetch_db(version, db_href, rhel=rhel, url_root=url_root, timeout=timeout, retries=retries)

    rpmvars = compute_rpmvars(version, rhel, arch, url_root)
    t = string.Template
    spec_path = os.path.join(cmsdist_dir.rstrip("/"), "rocm.spec")
    lines_in = read_rocm_spec(spec_path)

    new_lines: list[str] = [f"### RPM external rocm {version}\n"]
    oldversion = ""

    num_examined = 0
    num_changed = 0

    try:
        with contextlib.closing(open_sqlite(db_path)) as db:
            cur = db.cursor()
            for oldline in lines_in:
                line = oldline.strip()

                if line.startswith("### RPM"):
                    # remember prior version for name rewriting
                    parts = line.rsplit(maxsplit=1)
                    if len(parts) == 2:
                        oldversion = parts[1]
                    continue

                # Only transform SourceN lines that match the expected url prefix
                if not re.match(r"Source\d+:", line):
                    new_lines.append(oldline)
                    continue

                source, url = line.split(maxsplit=1)
                if not url.startswith("https://%{repository}/%{repoversion}"):
                    new_lines.append(oldline)
                    continue

                num_examined += 1

                # expand %{var} -> ${var} then substitute
                expanded_url = string.Template(url.replace("%{", "${")).substitute(rpmvars)

                # Is the exact href present?
                cur.execute("SELECT COUNT(*) FROM packages WHERE location_href=?", (expanded_url,))
                (count,) = cur.fetchone()
                if count != 0:
                    # exact match found
                    new_lines.append(oldline)
                    continue

                # Need to guess the package name from the URL filename.
                fname = expanded_url.rsplit("/", maxsplit=1)[-1]
                parts = fname.split("-")
                pname_parts = []
                for tmp in parts:
                    if tmp and tmp[0].isdigit():
                        break
                    pname_parts.append(tmp)
                if not pname_parts:
                    raise DatabaseError(f"Could not infer package name from {fname}")
                pname = "-".join(pname_parts)

                if oldversion:
                    pname = re.sub(re.escape(oldversion) + r"$", version, pname)

                cur.execute("SELECT location_href FROM packages WHERE name=?", (pname,))
                ret2 = cur.fetchone()
                if not ret2:
                    raise DatabaseError(f"No such package '{pname}' found in primary_db")

                found_href = ret2[0]
                # Normalize arch/rhel placeholders for the spec line
                p1 = re.escape(rpmvars["rhel"])
                p2 = re.escape(rpmvars["_arch"])
                newname = re.sub(rf"el{p1}\.{p2}\.rpm", "el%{rhel}.%{_arch}.rpm", found_href)

                new_line = f"{source} https://%{{repository}}/%{{repoversion}}/main/{newname}\n"
                if new_line != oldline:
                    num_changed += 1
                new_lines.append(new_line)
    finally:
        with contextlib.suppress(Exception):
            os.unlink(db_path)

    if dry_run:
        logging.info("[dry-run] Would write %d updated lines to %s (changed %d of %d SourceN items)",
                     len(new_lines), spec_path, num_changed, num_examined)
        return num_examined, num_changed

    try:
        atomic_write_with_backup(spec_path, new_lines)
    except Exception as e:
        raise SpecFileError(f"Failed to write updated spec to {spec_path}") from e

    logging.info("Updated %s (%d of %d SourceN entries changed). Backup at %s.bak",
                 spec_path, num_changed, num_examined, spec_path)
    return num_examined, num_changed


# --- CLI ---------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Update ROCm SourceN lines in rocm.spec")
    p.add_argument("version", help="New ROCm version, e.g. 6.2.1")
    p.add_argument("-c", "--cmsdist-dir", required=True, dest="dir",
                   help="Path to cmsdist directory (containing rocm.spec)")
    p.add_argument("--rhel", default=RHEL_DEFAULT, help=f"RHEL major version (default: {RHEL_DEFAULT})")
    p.add_argument("--arch", default=ARCH_DEFAULT, help=f"Architecture (default: {ARCH_DEFAULT})")
    p.add_argument("--url-root", default=URL_ROOT_DEFAULT, help=f"Repo base URL (default: {URL_ROOT_DEFAULT})")
    p.add_argument("--timeout", type=float, default=15.0, help="HTTP timeout seconds (default: 15)")
    p.add_argument("--retries", type=int, default=3, help="HTTP retries for transient errors (default: 3)")
    p.add_argument("-n", "--dry-run", action="store_true", help="Compute changes but do not modify rocm.spec")
    p.add_argument("-v", "--verbose", action="count", default=0,
                   help="Increase verbosity (-v, -vv)")
    return p


def configure_logging(verbosity: int) -> None:
    level = logging.WARNING
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    configure_logging(args.verbose)

    try:
        num_examined, num_changed = update_rocm(
            args.version,
            args.dir,
            rhel=args.rhel,
            arch=args.arch,
            url_root=args.url_root,
            timeout=args.timeout,
            retries=args.retries,
            dry_run=args.dry_run,
        )
        if args.dry_run:
            print(f"[dry-run] SourceN entries examined: {num_examined}; changes: {num_changed}")
        return 0
    except RocmUpdateError as e:
        logging.error("%s", e)
        return 2
    except Exception as e:
        logging.exception("Unexpected error: %s", e)
        return 3


if __name__ == "__main__":
    sys.exit(main())
