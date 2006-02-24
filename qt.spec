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

%prep
%setup -T -b %sourcepkg -n %n-%type-free-%{qtversion}

%build
unset QMAKESPEC || true
export QTDIR=$PWD
export PATH=$QTDIR/bin:$PATH
export LD_LIBRARY_PATH=$QTDIR/lib:$LD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=$QTDIR/lib:$DYLD_LIBRARY_PATH
echo yes | ./configure -prefix %i -thread -stl
# install_framework is hosed
perl -p -i -e 's/^install_framework:/install_framework:\ninstall_framework_no:/' src/Makefile
make
