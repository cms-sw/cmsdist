### RPM external python 2.6.8
## INITENV +PATH PATH %i/bin 
## INITENV +PATH LD_LIBRARY_PATH %i/lib
## INITENV SETV PYTHON_LIB_SITE_PACKAGES lib/python%{python_major_version}/site-packages
## INITENV SETV PYTHONHASHSEED random
# OS X patches and build fudging stolen from fink
%{expand:%%define python_major_version %(echo %realversion | cut -d. -f1,2)}
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)

Requires: expat bz2lib db4 gdbm

%if "%online" != "true"
Requires: zlib openssl sqlite
%endif

# FIXME: readline, crypt 
# FIXME: gmp, panel, tk/tcl, x11

Source0: http://www.python.org/ftp/%n/%realversion/Python-%realversion.tgz
Patch0: python-dont-detect-dbm
Patch1: python-fix-macosx-relocation
Patch2: python-2.6.8-ssl-fragment

%prep
%setup -n Python-%realversion
find . -type f | while read f; do
  if head -n1 $f | grep -q /usr/local; then
    perl -p -i -e "s|#!.*/usr/local/bin/python|#!/usr/bin/env python|" $f
  else :; fi
done
%patch0 -p0
%patch1 -p0
%patch2 -p1

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
%define extradirs $ZLIB_ROOT $OPENSSL_ROOT $SQLITE_ROOT 
%else
%define extradirs %{nil}
%endif

dirs="$EXPAT_ROOT $BZ2LIB_ROOT $NCURSES_ROOT $DB4_ROOT $GDBM_ROOT %{extradirs}" 

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

additionalConfigureOptions=""
case %cmsplatf in
    osx105* )
    additionalConfigureOptions="--disable-readline"
    ;;
esac

./configure --prefix=%i $additionalConfigureOptions --enable-shared \
            --without-tkinter --disable-tkinter

make %makeprocesses

%install
# We need to export it because setup.py now uses it to determine the actual
# location of DB4, this was needed to avoid having it picked up from the system.
export DB4_ROOT
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
                     %{i}/bin/python2.6-config \
                     %{i}/bin/smtpd.py \
                     %{i}/lib/python2.6/bsddb/dbshelve.py \
                     %{i}/lib/python2.6/test/test_bz2.py \
                     %{i}/lib/python2.6/test/test_largefile.py \
                     %{i}/lib/python2.6/test/test_optparse.py

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
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}lib/python2.6/config/Makefile
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
