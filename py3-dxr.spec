### RPM external py3-dxr 1.0.x
## INITENV +PATH PYTHON3PATH %i/${PYTHON3_LIB_SITE_PACKAGES}
Requires: zlib llvm sqlite
Requires: py3-Jinja2 py3-parsimonious py3-pysqlite3 py3-Pygments
%define dxrCommit d3c6e5b745c93b6e7788c734f7cb0dc14d957d37
%define branch cms/6ea764102a/clang18

Source0: git+https://github.com/cms-externals/dxr.git?obj=%{branch}/%{dxrCommit}&export=dxr-%{dxrCommit}&module=dxr-%dxrCommit&output=/dxr-%{dxrCommit}.tgz
%define keep_archives true

%prep
%setup -n dxr-%dxrCommit

%build
export SQLITE_ROOT
LDFLAGS="-L${ZLIB_ROOT}/lib" make %{makeprocesses}

%install
make %{makeprocesses} install PREFIX=%i
perl -p -i -e "s|^#!%{cmsroot}/.*|#!/usr/bin/env python3|" %{i}/bin/*.py
