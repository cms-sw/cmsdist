### RPM external python 2.4.2-CMS8
## INITENV +PATH PATH %i/bin 
## INITENV +PATH LD_LIBRARY_PATH %i/lib
# OS X patches and build fudging stolen from fink
Requires: zlib expat openssl bz2lib db4 gdbm
# FIXME: readline, crypt 
# FIXME: gmp, panel, tk/tcl, x11

Source0: http://www.python.org/ftp/%n/%realversion/Python-%realversion.tgz
Patch0: python-Include-pyport.h
Patch1: python-Lib-plat-mac-applesingle.py
Patch2: python-Lib-site.py
Patch3: python-Mac-OSX-Makefile
Patch4: python-Makefile.pre.in
Patch5: python-configure
Patch6: python-setup.py


%prep
%setup -n Python-%realversion
#%patch0
#%patch1
#%patch2
#%patch3
#%patch4
#%patch5
#%patch6
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
echo $dirs
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
%define pythonv %(echo %realversion | cut -d. -f 1,2)

#if [ $(uname) = Darwin ]; then
  # make install prefix=%i 
  # (cd Misc; /bin/rm -rf RPM)
  # mkdir -p %i/share/doc/%n
  # cp -R Demo Doc %i/share/doc/%n
  # cp -R Misc Tools %i/lib/python%{pythonv}
#  gcc -dynamiclib -all_load -single_module \
#    -framework System -framework CoreServices -framework Foundation \
#    %i/lib/python%{pythonv}/config/libpython%{pythonv}.a \
#    -undefined dynamic_lookup \
#    -o %i/lib/python%{pythonv}/config/libpython%{pythonv}.dylib \
#    -install_name %i/lib/python%{pythonv}/config/libpython%{pythonv}.dylib \
#    -current_version %{pythonv} -compatibility_version %{pythonv} -ldl
#  ln -s libpython%{pythonv}.dylib %i/lib/python%{pythonv}/config/libpython%{pythonv}.dylib # for boost
  # (cd %i/lib/python%{pythonv}/config; mv Makefile Makefile.orig;
  #  sed 's|-fno-common||g' < Makefile.orig > Makefile; /bin/rm -f Makefile.orig)
#fi

perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/idle \
                    %{i}/bin/pydoc \
                    %{i}/bin/smtpd.py \
                    %{i}/lib/python2.4/bsddb/dbshelve.py \
                    %{i}/lib/python2.4/test/test_bz2.py \
                    %{i}/lib/python2.4/test/test_largefile.py \
                    %{i}/lib/python2.4/test/test_optparse.py
# boost.spec rfio.spec
#
#
rm  `find %{i}/lib -maxdepth 1 -mindepth 1 ! -name '*python*'`
rm  `find %{i}/include -maxdepth 1 -mindepth 1 ! -name '*python*'`

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<lib name=python2.4>
<Client>
 <Environment name=PYTHON_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$PYTHON_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$PYTHON_BASE/include/python2.4"></Environment>
 <Environment name=PYTHON_COMPILE default="$PYTHON_BASE/lib/python2.4/compileall.py"></Environment>
</Client>
<use name=sockets>
<Runtime name=PATH value="$PYTHON_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

%post
find $RPM_INSTALL_PREFIX/%pkgrel/lib -type l | xargs ls -la | sed -e "s|.*[ ]\(/.*\) -> \(.*\)| \2 \1|;s|[ ]/[^ ]*/external| $RPM_INSTALL_PREFIX/%cmsplatf/external|g" | xargs -n2 ln -sf
%{relocateConfig}etc/scram.d/%n
