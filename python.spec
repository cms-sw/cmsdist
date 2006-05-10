### RPM external python 2.4.2
## INITENV +PATH PATH %i/bin 
## INITENV +PATH LD_LIBRARY_PATH %i/lib
# OS X patches and build fudging stolen from fink
Requires: zlib expat openssl bz2lib ncurses gdbm db4 glibc
# FIXME: readline, crypt 
# FIXME: gmp, panel, tk/tcl, x11

Source0: http://www.python.org/ftp/%n/%v/Python-%v.tgz
#Patch0: python-osx

%prep
%setup -n Python-%v
perl -p -i -e "s|#!.*/usr/local/bin/python|#!/usr/bin/env python|" Lib/cgi.py

%ifos darwin
 sed 's|@PREFIX@|%i|g' < %_sourcedir/python-osx | patch -p1
%endif

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
mkdir -p %i/include %i/lib
dirs="$ZLIB_ROOT $EXPAT_ROOT $OPENSSL_ROOT $BZ2LIB_ROOT $NCURSES_ROOT $DB4_ROOT $GDBM_ROOT"
for d in $dirs; do
  for f in $d/include/*; do
    [ -f $f ] || continue
    rm -f %i/include/$(basename $f)
    ln -s $f %i/include
  done
  for f in $d/lib/*; do
    [ -f $f ] || continue
    rm -f %i/lib/$(basename $f)
    ln -s $f %i/lib
  done
done

./configure --prefix=%i --enable-shared --without-tkinter --disable-tkinter --without-readline
make %makeprocesses

%install
make install
%define pythonv %(echo %v | cut -d. -f 1,2)

if [ $(uname) = Darwin ]; then
  # make install prefix=%i 
  # (cd Misc; /bin/rm -rf RPM)
  # mkdir -p %i/share/doc/%n
  # cp -R Demo Doc %i/share/doc/%n
  # cp -R Misc Tools %i/lib/python%{pythonv}
  cc -dynamiclib -all_load -single_module \
    -framework System -framework CoreServices -framework Foundation \
    %i/lib/python%{pythonv}/config/libpython%{pythonv}.a \
    -o %i/lib/python%{pythonv}/config/libpython%{pythonv}.dylib \
    -install_name %i/lib/python%{pythonv}/config/libpython%{pythonv}.dylib \
    -current_version %{pythonv} -compatibility_version %{pythonv} -ldl
  ln -s libpython%{pythonv}.dylib %i/lib/python%{pythonv}/config/libpython%{pythonv}.dylib # for boost
  # (cd %i/lib/python%{pythonv}/config; mv Makefile Makefile.orig;
  #  sed 's|-fno-common||g' < Makefile.orig > Makefile; /bin/rm -f Makefile.orig)
fi

perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/idle \
                    %{i}/bin/pydoc \
                    %{i}/bin/smtpd.py \
                    %{i}/lib/python2.4/bsddb/dbshelve.py \
                    %{i}/lib/python2.4/test/test_bz2.py \
                    %{i}/lib/python2.4/test/test_largefile.py \
                    %{i}/lib/python2.4/test/test_optparse.py
