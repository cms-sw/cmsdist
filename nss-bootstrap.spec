### RPM external nss-bootstrap 3.14.3
%define release_version %(echo "%{realversion}" | tr . _)_RTM
Source: https://ftp.mozilla.org/pub/mozilla.org/security/nss/releases/NSS_%{release_version}/src/nss-%{realversion}.tar.gz
Requires: nspr-bootstrap sqlite-bootstrap
Patch0: nss-3.14.3-add-SQLITE-LIBS-DIR
Patch1: nss-3.14.3-add-ZLIB-LIBS-DIR-and-ZLIB-INCLUDE-DIR

%define isamd64 %(case %{cmsplatf} in (*amd64*|*_mic_*) echo 1 ;; (*) echo 0 ;; esac)

Requires: zlib-bootstrap

%prep
%setup -n nss-%{realversion}
%patch0 -p1
%patch1 -p1

%build
export NSPR_INCLUDE_DIR="${NSPR_BOOTSTRAP_ROOT}/include/nspr"
export NSPR_LIB_DIR="${NSPR_BOOTSTRAP_ROOT}/lib"
export USE_SYSTEM_ZLIB=1
export ZLIB_INCLUDE_DIR="${ZLIB_BOOTSTRAP_ROOT}/include"
export ZLIB_LIBS_DIR="${ZLIB_BOOTSTRAP_ROOT}/lib"
export NSS_USE_SYSTEM_SQLITE=1
export SQLITE_INCLUDE_DIR="${SQLITE_BOOTSTRAP_ROOT}/include"
export SQLITE_LIBS_DIR="${SQLITE_BOOTSTRAP_ROOT}/lib"
%if %isamd64
export USE_64=1
%endif

make -C ./mozilla/security/coreconf clean
make -C ./mozilla/security/dbm clean
make -C ./mozilla/security/nss clean
make -C ./mozilla/security/coreconf
make -C ./mozilla/security/dbm
make -C ./mozilla/security/nss

%install
case %{cmsplatf} in
  osx*)
    soname=dylib ;;
  *)
    soname=so ;;
esac
rm -rf %{i}/lib/libsoftokn3*
rm -rf %{i}/lib/libsql*
rm -rf %{i}/lib/libfreebl3*

install -d %{i}/include/nss3
install -d %{i}/lib
find mozilla/dist/public/nss -name '*.h' -exec install -m 644 {} %{i}/include/nss3 \;
find . -path "*/mozilla/dist/*.OBJ/lib/*.${soname}" -exec install -m 755 {} %{i}/lib \;
%define strip_files %{i}/lib
