### RPM external python 2.7.16
## INITENV +PATH PATH %{i}/bin
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib
## INITENV SETV PYTHON_LIB_SITE_PACKAGES lib/python%{python_major_version}/site-packages
## INITENV SETV PYTHONHASHSEED random
# OS X patches and build fudging stolen from fink
%{expand:%%define python_major_version %(echo %realversion | cut -d. -f1,2)}
Provides: python(abi)
Requires: expat bz2lib db6 gdbm libffi
Requires: zlib sqlite

# FIXME: readline, crypt 
# FIXME: gmp, panel, x11
%define tag 583c0f2237aade97173702ac602b16f51eadde6d
%define branch cms/2.7/c40eeeb
%define github_user cms-externals
Source0: git+https://github.com/%github_user/cpython.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Source1: valgrind-python.supp

%prep
%setup -b 0 -n python-%{realversion}

find . -type f | while read f; do
  if head -n1 $f | grep -q /usr/local; then
    perl -p -i -e "s|#!.*/usr/local/bin/python|#!/usr/bin/env python|" $f
  else :; fi
done

rm -rf Modules/expat || exit 1
rm -rf Modules/zlib || exit 1
for SUBDIR in darwin libffi libffi_arm_wince libffi_msvc libffi_osx ; do
  rm -rf Modules/_ctypes/$SUBDIR || exit 1 ;
done
for FILE in md5module.c md5.c shamodule.c sha256module.c sha512module.c ; do
  rm -f Modules/$FILE || exit 1
done

%build
# Python is awkward about passing other include or library directories
# to it.  Basically there is no way to pass anything from configure to
# make, or down to python itself.  To get python detect the extensions
# we want to enable, we simply have to link the contents into python's
# own include/lib directories.  Ugh.
#
# NB: It would sort-of make sense to link more stuff from /sw on OS X,
# but we simply cannot link the whole world.  If you need something,
# see above for the commented-out list of packages that could be
# linked specifically, or could be built by ourselves, depending on
# whether we like to pick up system libraries or want total control.

mkdir -p %{i}/{include,lib,bin}

dirs="${EXPAT_ROOT} ${BZ2LIB_ROOT} ${DB6_ROOT} ${GDBM_ROOT} ${LIBFFI_ROOT} ${ZLIB_ROOT} ${SQLITE_ROOT}"

# We need to export it because setup.py now uses it to determine the actual
# location of DB4, this was needed to avoid having it picked up from the system.
export DB6_ROOT
export LIBFFI_ROOT

# Python's configure parses LDFLAGS and CPPFLAGS to look for aditional library and include directories
echo $dirs
LDFLAGS=""
CPPFLAGS=""
for d in $dirs; do
  LDFLAGS="$LDFLAGS -L$d/lib -L$d/lib64"
  CPPFLAGS="$CPPFLAGS -I$d/include"
done
export LDFLAGS
export CPPFLAGS

# Bugfix for dbm package. Use ndbm.h header and gdbm compatibility layer.
sed -ibak "s/ndbm_libs = \[\]/ndbm_libs = ['gdbm', 'gdbm_compat']/" setup.py

sed -ibak "s|LIBFFI_INCLUDEDIR=.*|LIBFFI_INCLUDEDIR=\"${LIBFFI_ROOT}/include\"|g" configure

./configure \
  --prefix=%{i} \
  --enable-shared \
  --with-system-ffi \
  --with-system-expat --enable-unicode=ucs4 \
  $additionalConfigureOptions

# Modify pyconfig.h to match macros from GLIBC features.h on Linux machines.
# _POSIX_C_SOURCE and _XOPEN_SOURCE macros are not identical anymore
# starting GLIBC 2.10.1. Python.h is not included before standard headers
# in CMSSW and pyconfig.h is not smart enough to detect already defined
# macros on Linux. The following problem does not exists on BSD machines as
# cdefs.h does not define these macros.
case %cmsplatf in
  osx*);;
  *)
    rm -f cms_configtest.cpp
    cat <<CMS_EOF > cms_configtest.cpp
#include <features.h>

int main() {
  return 0;
}
CMS_EOF

    FEATURES=$(g++ -dM -E -DGNU_GCC=1 -D_GNU_SOURCE=1 -D_DARWIN_SOURCE=1 cms_configtest.cpp \
      | grep -E '_POSIX_C_SOURCE |_XOPEN_SOURCE ')
    rm -f cms_configtest.cpp a.out

    POSIX_C_SOURCE=$(echo "${FEATURES}" | grep _POSIX_C_SOURCE | cut -d ' ' -f 3)
    XOPEN_SOURCE=$(echo "${FEATURES}" | grep _XOPEN_SOURCE | cut -d ' ' -f 3)

    sed -ibak "s/\(#define _POSIX_C_SOURCE \)\(.*\)/\1${POSIX_C_SOURCE}/g" pyconfig.h
    sed -ibak "s/\(#define _XOPEN_SOURCE \)\(.*\)/\1${XOPEN_SOURCE}/g" pyconfig.h
  ;;
esac

# Modify pyconfig.h to disable GCC format attribute as it is used incorrectly.
# Triggers an error if -Werror=format is used with GNU GCC 4.8.0+.
sed -ibak "s/\(#define HAVE_ATTRIBUTE_FORMAT_PARSETUPLE .*\)/\/* \1 *\//g" pyconfig.h

# Python does not support parallel builds because of bug:
# https://bugs.python.org/issue22359
# Note, the problem is solved upstream (3.5)
make

%install
# We need to export it because setup.py now uses it to determine the actual
# location of DB4, this was needed to avoid having it picked up from the system.
export DB6_ROOT
export LIBFFI_ROOT

make install
%define pythonv %(echo %realversion | cut -d. -f 1,2)

case %cmsplatf in
  osx*)
   make install prefix=%i 
   (cd Misc; /bin/rm -rf RPM)
   mkdir -p %i/share/doc/%n
   cp -R Demo Doc %i/share/doc/%n
   cp -R Misc Tools %i/lib/python%{pythonv}
   gcc -dynamiclib -all_load -single_module \
    -framework System -framework CoreServices -framework Foundation \
    %i/lib/python%{pythonv}/config/libpython%{pythonv}.a \
    -undefined dynamic_lookup \
    -o %i/lib/python%{pythonv}/config/libpython%{pythonv}.dylib \
    -install_name %i/lib/python%{pythonv}/config/libpython%{pythonv}.dylib \
    -current_version %{pythonv} -compatibility_version %{pythonv} -ldl
   (cd %i/lib/python%{pythonv}/config
    perl -p -i -e 's|-fno-common||g' Makefile)

   find %i/lib/python%{pythonv}/config -name 'libpython*' -exec mv -f {} %i/lib \;
  ;;
esac

 perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/idle \
                     %{i}/bin/pydoc \
                     %{i}/bin/python-config \
                     %{i}/bin/2to3 \
                     %{i}/bin/python2.7-config \
                     %{i}/bin/smtpd.py

find %{i}/lib -maxdepth 1 -mindepth 1 ! -name '*python*' -exec rm {} \;
find %{i}/include -maxdepth 1 -mindepth 1 ! -name '*python*' -exec rm {} \;

# remove executable permission anything which is *.py script,
# is executable, but does not start with she-bang so not valid
# executable; this avoids problems with rpm 4.8+ find-requires
find %i -name '*.py' -perm +0111 | while read f; do
  if head -n1 $f | grep -q '"'; then chmod -x $f; else :; fi
done

# Remove documentation, examples and test files. 
%define drop_files { %{i}/lib/python%{pythonv}/test \
                   %{i}/lib/python%{pythonv}/distutils/tests \
                   %{i}/lib/python%{pythonv}/json/tests \
                   %{i}/lib/python%{pythonv}/ctypes/test \
                   %{i}/lib/python%{pythonv}/sqlite3/test \
                   %{i}/lib/python%{pythonv}/bsddb/test \
                   %{i}/lib/python%{pythonv}/email/test \
                   %{i}/lib/python%{pythonv}/lib2to3/tests \
                   %{i}/lib/pkgconfig }

rm -rf %{i}/share
mkdir -p %{i}/share/valgrind
cp %{SOURCE1} %{i}/share/valgrind/valgrind-python.supp

# Remove .pyo files
find %i -name '*.pyo' -exec rm {} \;

echo "from os import environ" > %i/lib/python2.7/sitecustomize.py
echo "if 'PYTHON27PATH' in environ:" >> %i/lib/python2.7/sitecustomize.py
echo "   import os,site" >> %i/lib/python2.7/sitecustomize.py
echo "   for p in environ['PYTHON27PATH'].split(os.pathsep):">> %i/lib/python2.7/sitecustomize.py
echo "       site.addsitedir(p)">> %i/lib/python2.7/sitecustomize.py


%post
%{relocateConfig}lib/python2.7/config/Makefile
%{relocateConfig}lib/python2.7/_sysconfigdata.py
