### RPM external java-jdk 1.7.0_79
# Linux only; OS X ships java on system which we use instead
Requires: libxml2
%ifnos darwin
Provides: libXtst.so.6()(64bit)
Provides: libXxf86vm.so.1()(64bit)
Provides: libasound.so.2()(64bit)
Provides: libatk-1.0.so.0()(64bit)
Provides: libavcodec.so.52()(64bit)
Provides: libavcodec.so.53()(64bit)
Provides: libavformat.so.52()(64bit)
Provides: libavformat.so.53()(64bit)
Provides: libcairo.so.2()(64bit)
Provides: libgdk-x11-2.0.so.0()(64bit)
Provides: libgdk_pixbuf-2.0.so.0()(64bit)
Provides: libgio-2.0.so.0()(64bit)
Provides: libglib-2.0.so.0()(64bit)
Provides: libgmodule-2.0.so.0()(64bit)
Provides: libgobject-2.0.so.0()(64bit)
Provides: libgthread-2.0.so.0()(64bit)
Provides: libgtk-x11-2.0.so.0()(64bit)
Provides: libpango-1.0.so.0()(64bit)
Provides: libpangocairo-1.0.so.0()(64bit)
Provides: libpangoft2-1.0.so.0()(64bit)
Provides: libxslt.so.1()(64bit)
Provides: libasound.so.2(ALSA_0.9)(64bit)
Provides: libasound.so.2(ALSA_0.9.0rc4)(64bit)
Provides: libavcodec.so.52(LIBAVCODEC_52)(64bit)
Provides: libavcodec.so.53(LIBAVCODEC_53)(64bit)
Provides: libavformat.so.52(LIBAVFORMAT_52)(64bit)
Provides: libavformat.so.53(LIBAVFORMAT_53)(64bit)
Provides: libxslt.so.1(LIBXML2_1.0.11)(64bit)
Provides: libxslt.so.1(LIBXML2_1.0.22)(64bit)
Provides: libxslt.so.1(LIBXML2_1.0.24)(64bit)
Provides: libxslt.so.1(LIBXML2_1.1.9)(64bit)

Source0: http://cmsrep.cern.ch/cmssw/oracle-mirror/20150922-jdk-7u79-linux-x64.tar.gz
%endif

%prep
%ifnos darwin
%setup -T -b 0 -n jdk1.7.0_79
%define javadir jdk1.7.0_79
%endif
%build

%install
%ifnos darwin
ls -l
cp -r * %i
rm -rf %i/man
%endif
