### RPM external qt 3.3.8-CMS19
## INITENV UNSET QMAKESPEC
## INITENV SET QTDIR %i
%define qttype %(echo %realversion | sed 's/[-0-9.]*//')
%define qtversion %(echo %realversion | sed 's/-.*//')
%if "%qttype" == ""
 %ifos darwin
  %define type	mac
 %else
  %define type	x11
 %endif
%else
 %define type	%{qttype}
%endif

%if "%type" == "x11"
 %define sourcepkg 1
%else
 %define sourcepkg 0
%endif

# Requires: zlib, ...
Source0: ftp://ftp.trolltech.com/qt/source/%n-mac-free-%{qtversion}.tar.bz2
Source1: ftp://ftp.trolltech.com/qt/source/%n-x11-free-%{qtversion}.tar.bz2
Patch0: qt-mkspecs-qmake.conf
Patch1: qt-mkspecs-qplatformdefs.h
Patch2: qt-src-kernel-qaccessible_mac.cpp
Patch3: qt-src-qt_install.pri
Patch4: qt-mkspecs-qmake.conf_2
Patch5: qt3-leopard

%prep
%setup -T -b %sourcepkg -n %n-%type-free-%{qtversion}
#%ifos darwin
#%patch1 -p0
#%patch2 -p0
#%patch3 -p0
#%endif

case %cmsplatf in
    slc4_ia32* )
        # The kludge supports the libfontconfig kludge described below
%patch4 -p1
    ;;
    osx105* )
%patch5 -p1
    ;;
esac

%build
unset QMAKESPEC || true
export QTDIR=$PWD
export PATH=$QTDIR/bin:$PATH
export LD_LIBRARY_PATH=$QTDIR/lib:$LD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=$QTDIR/lib:$DYLD_LIBRARY_PATH

case $(uname -m) in
  x86_64)
    export CONFIG_ARGS="-platform linux-g++-64"
esac

echo yes | ./configure -prefix %i -thread -stl $CONFIG_ARGS
# install_framework is hosed
perl -p -i -e 's/^install_framework:/install_framework:\ninstall_framework_no:/' src/Makefile
# The following is a kludge around the fact that the fact that the 
# /usr/lib/libfontconfig.so soft link (for 32-bit lib) is missing
# on the 64-bit machines
%if (("%cmsplatf" == "slc4_ia32_gcc345")||("%cmsplatf" == "slc4_ia32_gcc412")||("%cmsplatf" == "slc4_ia32_gcc422"))
  mkdir -p %{_builddir}/lib
  ln -s /usr/lib/libfontconfig.so.1 %{_builddir}/%n-%type-free-%{qtversion}/lib/libfontconfig.so
%endif

make %makeprocesses

%install
make install

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<info url="http://www.trolltech.com/products/qt.html"></info>
<LIB name=qt-mt>
<Client>
 <Environment name=QT_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$QT_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$QT_BASE/include"></Environment>
</Client>
<Flags CPPDEFINES="QT_ALTERNATE_QTSMANIP QT_CLEAN_NAMESPACE QT_THREAD_SUPPORT">
<Runtime name=PATH value="$QT_BASE/bin" type=path>
<use name=X11>
<use name=opengl>
<use name=zlib>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}lib/libqt-mt.la
%{relocateConfig}etc/scram.d/%n

