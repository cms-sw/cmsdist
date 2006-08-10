### RPM external qt 3.3.4
## INITENV UNSET QMAKESPEC
## INITENV SET QTDIR %i
%define qttype %(echo %v | sed 's/[-0-9.]*//')
%define qtversion %(echo %v | sed 's/-.*//')
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

%prep
%setup -T -b %sourcepkg -n %n-%type-free-%{qtversion}
%ifos darwin
%patch1 -p0
%patch2 -p0
%patch3 -p0
%endif

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
make %makeprocesses
#
