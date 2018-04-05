### RPM external python3 3.6.4
## INITENV +PATH PATH %{i}/bin
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib
## INITENV SETV PYTHON3_LIB_SITE_PACKAGES lib/python%{pythonv}/site-packages
## INITENV SETV PYTHON3HASHSEED random
# OS X patches and build fudging stolen from fink
%define pythonv %(echo %realversion | cut -d. -f 1,2)
%define python_major %(echo %realversion | cut -d. -f 1)

Requires: expat bz2lib db6 gdbm openssl libffi zlib sqlite

Source: https://www.python.org/ftp/python/%realversion/Python-%realversion.tgz

%prep
%setup -n Python-%{realversion}

%build
mkdir -p %{i}/{include,lib,bin}

# We need to export it because setup.py now uses it to determine the actual
# location of DB4, this was needed to avoid having it picked up from the system.
export DB6_ROOT
export LIBFFI_ROOT

# Python's configure parses LDFLAGS and CPPFLAGS to look for aditional library and include directories
LDFLAGS=""
CPPFLAGS=""
for d in ${EXPAT_ROOT} ${BZ2LIB_ROOT} ${DB6_ROOT} ${GDBM_ROOT} ${OPENSSL_ROOT} ${LIBFFI_ROOT} ${ZLIB_ROOT} ${SQLITE_ROOT}; do
  LDFLAGS="$LDFLAGS -L$d/lib -L$d/lib64"
  CPPFLAGS="$CPPFLAGS -I$d/include"
done

./configure \
  --prefix=%{i} \
  --enable-shared \
  --enable-ipv6 \
  --with-system-ffi \
  --without-ensurepip \
  --with-system-expat \
  LDFLAGS="$LDFLAGS" \
  CPPFLAGS="$CPPFLAGS"

make %{makeprocesses}

%install
make %{makeprocesses} install
sed -i -e "s|^#!.*python%{pythonv} *$|#!/usr/bin/env python%{python_major}|" %{i}/bin/* %{i}/lib/python*/*.py
sed -i -e 's|^#!/.*|#!/usr/bin/env python%{pythonv}m|' %{i}/lib/python*/config-*/python-config.py
sed -i -e 's|^#! */usr/local/bin/python|#!/usr/bin/env python|' %{i}/lib/python*/cgi.py

# is executable, but does not start with she-bang so not valid
# executable; this avoids problems with rpm 4.8+ find-requires
find %i -name '*.py' -perm +0111 | while read f; do
  if head -n1 $f | grep -q '"'; then chmod -x $f; else :; fi
done

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test \$?$root != 0 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

# Remove .pyo files
find %i -name '*.pyo' -exec rm {} \;

# Remove documentation, examples and test files.
rm -rf %{i}/share %{i}/lib/python*/test %{i}/lib/python%{pythonv}/distutils/tests %{i}/lib/python%{pythonv}/lib2to3/tests

echo "from os import environ" > %i/lib/python%{pythonv}/sitecustomize.py
echo "if 'PYTHON3PATH' in environ:" >> %i/lib/python%{pythonv}/sitecustomize.py
echo "   import os,site" >> %i/lib/python%{pythonv}/sitecustomize.py
echo "   for p in environ['PYTHON3PATH'].split(os.pathsep):">> %i/lib/python%{pythonv}/sitecustomize.py
echo "       site.addsitedir(p)">> %i/lib/python%{pythonv}/sitecustomize.py




%post
%{relocateConfig}bin/python*-config
%{relocateConfig}lib/pkgconfig/python*.pc
%{relocateConfig}lib/python*/config-*/Makefile
%{relocateConfig}lib/python*/_sysconfigdata*.py
%{relocateConfig}etc/profile.d/dependencies-setup.csh
%{relocateConfig}etc/profile.d/dependencies-setup.sh
