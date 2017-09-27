### RPM external python3 3.6.2
## INITENV +PATH PATH %i/bin 
## INITENV +PATH LD_LIBRARY_PATH %i/lib
## INITENV SETV PYTHON_LIB_SITE_PACKAGES lib/python%{python_major_version}/site-packages
## INITENV SETV PYTHONHASHSEED random
# OS X patches and build fudging stolen from fink
%{expand:%%define python_major_version %(echo %realversion | cut -d. -f1,2)}
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)

Requires: expat bz2lib db4 gdbm

%if "%online" != "true"
Requires: zlib openssl sqlite readline ncurses
%endif

Source: https://www.python.org/ftp/python/%realversion/Python-%realversion.tgz

%prep
%setup -n Python-%realversion

find . -type f | while read f; do
  if head -n1 $f | grep -q /usr/local; then
    perl -p -i -e "s|#!.*/usr/local/bin/python|#!/usr/bin/env python3|" $f
  else :; fi
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
#mkdir -p %i/include %i/lib
mkdir -p %i/include %i/lib %i/bin

%if "%online" != "true"
%define extradirs ${ZLIB_ROOT} ${OPENSSL_ROOT} ${SQLITE_ROOT}
%else
%define extradirs %{nil}
%endif

# We need to export it because setup.py now uses it to determine the actual
# location of DB4, this was needed to avoid having it picked up from the system.
export DB4_ROOT
export READLINE_ROOT
export NCURSES_ROOT

dirs="${EXPAT_ROOT} ${BZ2LIB_ROOT} ${NCURSES_ROOT} ${DB4_ROOT} ${GDBM_ROOT} ${READLINE_ROOT} %{extradirs}"

# Python's configure parses LDFLAGS and CPPFLAGS to look for aditional library and include directories
echo $dirs
LDFLAGS=""
CPPFLAGS=""
for d in $dirs; do
  LDFLAGS="$LDFLAGS -L$d/lib"
done
for d in $dirs $READLINE_ROOT $NCURSES_ROOT; do
  CPPFLAGS="$CPPFLAGS -I$d/include"
done
LDFLAGS="$LDFLAGS $NCURSES_ROOT/lib/libncurses.a $READLINE_ROOT/lib/libreadline.a"
export LDFLAGS
export CPPFLAGS

# Bugfix for dbm package. Use ndbm.h header and gdbm compatibility layer.
sed -ibak "s/ndbm_libs = \[\]/ndbm_libs = ['gdbm', 'gdbm_compat']/" setup.py

./configure --prefix=%i --enable-shared \
            --enable-unicode=ucs4 --enable-optimizations \
            --without-tkinter --disable-tkinter

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

make %makeprocesses

%install
# We need to export it because setup.py now uses it to determine the actual
# location of DB4, this was needed to avoid having it picked up from the system.
export DB4_ROOT
export READLINE_ROOT
export NCURSES_ROOT

make install
%define pythonv %(echo %realversion | cut -d. -f 1,2)
%define python_major %(echo %realversion | cut -d. -f 1)

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

perl -p -i -e "s|^#!.*python3.6|#!/usr/bin/env python3|" \
                    %{i}/bin/idle%{pythonv} \
                    %{i}/bin/pydoc%{pythonv} \
                    %{i}/bin/pip%{pythonv} \
                    %{i}/bin/pip3 \
                    %{i}/bin/easy_install-%{pythonv} \
                    %{i}/bin/pyvenv-%{pythonv} \
                    %{i}/bin/python%{pythonv}-config \
                    %{i}/bin/2to3-%{pythonv} \
                    %{i}/bin/python%{pythonv}-config \
                    %{i}/bin/python%{pythonv}m-config \
                    %{i}/lib/python%{pythonv}/_sysconfigdata_m_linux_x86_64-linux-gnu.py \
                    %{i}/lib/python%{pythonv}/config-%{pythonv}m-x86_64-linux-gnu/python-config.py

echo "RPM_BUILD_ROOT=$RPM_BUILD_ROOT"
sed -i -e "s|$RPM_BUILD_ROOT||" \
                    %{i}/lib/python%{pythonv}/_sysconfigdata_m_linux_x86_64-linux-gnu.py
sed -i -e "s|$RPM_BUILD_ROOT||" \
                    %{i}/bin/python%{python_major}-config
sed -i -e "s|$RPM_BUILD_ROOT||" \
                    %{i}/bin/python%{pythonv}-config
sed -i -e "s|$RPM_BUILD_ROOT||" \
                    %{i}/bin/python%{pythonv}m-config
sed -i -e "s|$RPM_BUILD_ROOT||" \
                    %{i}/lib/python%{pythonv}/config-%{pythonv}m-x86_64-linux-gnu/python-config.py
sed -i -e "s|$RPM_BUILD_ROOT||" \
                     %{i}/lib/python%{pythonv}/config-%{pythonv}m-x86_64-linux-gnu/Makefile

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

# add python -> python3 link
cd %i/bin
ln -s python3 python
cd -

# generate dependency
%addDependency

%post
%{relocateConfig}lib/python3.6/config/Makefile
%{relocateConfig}lib/python3.6/_sysconfigdata.py
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
