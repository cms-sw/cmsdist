### RPM external kcachegrind 0.4.6-cmsp1
Provides: libDCOP.so.4
Provides: libart_lgpl_2.so.2
Provides: libfam.so.0
Provides: libkdecore.so.4
Provides: libkdefx.so.4
Provides: libkdesu.so.4
Provides: libkdeui.so.4
Provides: libkio.so.4
Provides: libkwalletclient.so.1
Requires: qt libpng

%define realversion %(echo %v | cut -d- -f1)
%define machine_os  %(echo %cmsplatf | cut -d_ -f1)
%if "%{machine_os}" == "slc4"
%define sourcefile0 http://kcachegrind.sourceforge.net/%{n}-%{realversion}.tar.gz
%define pacthfile0 http://cmsdoc.cern.ch/~muzaffar/public/%{n}-%{realversion}-patch.tar.gz
%else
%define sourcefile0   none
%define pacthfile0    none
%endif

Source0: %sourcefile0
Source1: %pacthfile0

%prep
%if "%{machine_os}" == "slc4"
%setup -T -b 1 -n %{n}-%{realversion}-patch
%setup -T -b 0 -n %{n}-%{realversion}
# CMS patch
cp -fp %{_builddir}/%{n}-%{realversion}-patch/functionnameanalyzer.* %{_builddir}/%n-%realversion/kcachegrind/
patch -u %{_builddir}/%n-%realversion/kcachegrind/tracedata.cpp %{_builddir}/%{n}-%{realversion}-patch/tracedata.cpp.patch
patch -u %{_builddir}/%n-%realversion/kcachegrind/Makefile.am %{_builddir}/%{n}-%{realversion}-patch/Makefile.am.patch
make -f admin/Makefile.common cvs
%endif

%build
%if "%{machine_os}" == "slc4"
export CPPFLAGS="-I$LIBPNG_ROOT/include"
export LDFLAGS="-L$LIBPNG_ROOT/lib"
./configure --prefix=%i --disable-rpath

# Fix for hard coded rpath
sed 's|hardcode_libdir_flag_spec=".*"|hardcode_libdir_flag_spec=""|' libtool > libtool.new
mv libtool.new libtool

make %makeprocesses
%install
make install
%endif
%post
%if "%{machine_os}" != "slc4"
mkdir -p $RPM_INSTALL_PREFIX/%pkgrel/bin
cat << \EOF_KCACHEGRIND > $RPM_INSTALL_PREFIX/%pkgrel/bin/kcachegrind
#!/bin/sh
echo "WARNING: KCachegrind is only available for SLC4"
EOF_KCACHEGRIND
chmod 755 $RPM_INSTALL_PREFIX/%pkgrel/bin/kcachegrind
%endif
