### RPM external python 2.7.3
## INITENV +PATH PATH %i/bin
## INITENV +PATH LD_LIBRARY_PATH %i/lib
## INITENV SETV PYTHON_LIB_SITE_PACKAGES lib/python%{python_major_version}/site-packages
## INITENV SETV PYTHONHASHSEED random
# OS X patches and build fudging stolen from fink
%{expand:%%define python_major_version %(echo %realversion | cut -d. -f1,2)}

%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%define hostpython %{nil}
%if "%mic" == "true"
Requires: icc
%define hostpython_dir %{_builddir}/Python-%{realversion}.host
%define hostpython HOSTPYTHON="LD_PRELOAD=%{hostpython_dir}/libpython%{python_major_version}.so.1.0 %{hostpython_dir}/python" HOSTPGEN="LD_PRELOAD=%{hostpython_dir}/libpython%{python_major_version}.so.1.0 %{hostpython_dir}/Parser/pgen" CROSS_COMPILE=k1om- CROSS_COMPILE_TARGET=yes HOSTARCH=k1om BUILDARCH=x86_64-linux-gnu
%endif
%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)
%define isnotonline %(case %{cmsplatf} in (*onl_*_*) echo 0 ;; (*) echo 1 ;; esac)

Requires: expat bz2lib db4 gdbm openssl

%if %isnotonline
Requires: zlib sqlite readline
%endif

# FIXME: readline, crypt
# FIXME: gmp, panel, tk/tcl, x11

Source0: http://www.python.org/ftp/%n/%realversion/Python-%realversion.tgz
Source1: python-2.7.3-xcompile
Patch0: python-2.7.3-dont-detect-dbm
Patch1: python-fix-macosx-relocation
Patch2: python-2.7.3-fix-pyport
Patch3: python-2.7.3-ssl-fragment

%prep
%if "%mic" == "true"
rm -rf %{hostpython_dir}
%endif

%setup -n Python-%realversion
find . -type f | while read f; do
  if head -n1 $f | grep -q /usr/local; then
    perl -p -i -e "s|#!.*/usr/local/bin/python|#!/usr/bin/env python|" $f
  else :; fi
done
%patch0 -p1
%patch1 -p0

%if %isdarwin
%patch2 -p1
%endif

%patch3 -p1

%build
# Python is awkward about passing other include or library directories
# to it. Basically there is no way to pass anything from configure to
# make, or down to python itself. To get python detect the extensions
# we want to enable, we simply have to link the contents into python's
# own include/lib directories. Ugh.
#
# NB: It would sort-of make sense to link more stuff from /sw on OS X,
# but we simply cannot link the whole world. If you need something,
# see above for the commented-out list of packages that could be
# linked specifically, or could be built by ourselves, depending on
# whether we like to pick up system libraries or want total control.
#mkdir -p %i/include %i/lib
mkdir -p %i/include %i/lib %i/bin

%if %isnotonline
%define extradirs ${ZLIB_ROOT} ${SQLITE_ROOT} ${READLINE_ROOT}
%else
%define extradirs %{nil}
%endif

dirs="${EXPAT_ROOT} ${BZ2LIB_ROOT} ${DB4_ROOT} ${GDBM_ROOT} ${OPENSSL_ROOT} %{extradirs}"

# We need to export it because setup.py now uses it to determine the actual
# location of DB4, this was needed to avoid having it picked up from the system.
export DB4_ROOT

# Python's configure parses LDFLAGS and CPPFLAGS to look for aditional library and include directories
echo $dirs
LDFLAGS=""
CPPFLAGS=""
for d in $dirs; do
  LDFLAGS="$LDFLAGS -L $d/lib"
  CPPFLAGS="$CPPFLAGS -I $d/include"
done
export LDFLAGS
export CPPFLAGS

# Bugfix for dbm package. Use ndbm.h header and gdbm compatibility layer.
sed -ibak "s/ndbm_libs = \[\]/ndbm_libs = ['gdbm', 'gdbm_compat']/" setup.py

./configure --prefix=%i $additionalConfigureOptions --enable-shared

%define cxx g++
%if "%mic" == "true"
%define cxx icpc -mmic
make %makeprocesses
cp -r %{_builddir}/Python-%{realversion} %{hostpython_dir}
make distclean
patch -p1 < %{_sourcedir}/python-2.7.3-xcompile
./configure --prefix=%i $additionalConfigureOptions --enable-shared CC="icc -mmic" CXX="%{cxx}" --host=x86_64 --without-gcc
%endif

# Modify pyconfig.h to match macros from GLIBC features.h on Linux machines.
# _POSIX_C_SOURCE and _XOPEN_SOURCE macros are not identical anymore
# starting GLIBC 2.10.1. Python.h is not included before standard headers
# in CMSSW and pyconfig.h is not smart enough to detect already defined
# macros on Linux. The following problem does not exists on BSD machines as
# cdefs.h does not define these macros.
case %cmsplatf in
  slc6*|fc*)
    rm -f cms_configtest.cpp
    cat <<CMS_EOF > cms_configtest.cpp
#include <features.h>

int main() {
  return 0;
}
CMS_EOF

    FEATURES=$(%cxx -dM -E -DGNU_GCC=1 -D_GNU_SOURCE=1 -D_DARWIN_SOURCE=1 cms_configtest.cpp \
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

make %makeprocesses %{hostpython}

%install
# We need to export it because setup.py now uses it to determine the actual
# location of DB4, this was needed to avoid having it picked up from the system.
export DB4_ROOT
make install %{hostpython}
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

# remove tkinter that brings dependency on libtk:
find %{i}/lib -type f -name "_tkinter.so" -exec rm {} \;

# Remove documentation, examples and test files.
%define drop_files { %i/share %{i}/lib/python%{pythonv}/test \
                   %{i}/lib/python%{pythonv}/distutils/tests \
                   %{i}/lib/python%{pythonv}/json/tests \
                   %{i}/lib/python%{pythonv}/ctypes/test \
                   %{i}/lib/python%{pythonv}/sqlite3/test \
                   %{i}/lib/python%{pythonv}/bsddb/test \
                   %{i}/lib/python%{pythonv}/email/test \
                   %{i}/lib/python%{pythonv}/lib2to3/tests }

# Remove .pyo files
find %i -name '*.pyo' -exec rm {} \;

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%if "%mic" == "true"
mkdir %i/host
cp %{hostpython_dir}/python %i/host
cp %{hostpython_dir}/libpython%{python_major_version}.so.1.0 %i/host
echo '#!/bin/sh' > %i/host/hostpython
echo 'LD_PRELOAD=%{i}/host/libpython%{python_major_version}.so.1.0 %{i}/host/python $@' >> %i/host/hostpython
chmod +x %i/host/hostpython
%endif

%post
%{relocateConfig}lib/python%{python_major_version}/config/Makefile
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
%if "%mic" == "true"
%{relocateConfig}host/hostpython
%endif
