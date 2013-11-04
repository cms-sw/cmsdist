### RPM external java-jdk 1.5.0_15
# Linux only; OS X ships java on system which we use instead

%ifos darwin
Source: none

%else
Provides: libasound.so.2
Provides: libasound.so.2(ALSA_0.9)
Provides: libjava_crw_demo_g.so
Provides: libodbc.so
Provides: libodbcinst.so
# 64 bit versions
Provides: libasound.so.2()(64bit)
Provides: libasound.so.2(ALSA_0.9)(64bit)
Provides: libjava_crw_demo_g.so()(64bit)
Provides: libodbc.so()(64bit)
Provides: libodbcinst.so()(64bit)
Provides: libXp.so.6()(64bit)
Provides: libXt.so.6()(64bit)
Provides: libXtst.so.6()(64bit)

%define downloadv %(echo %realversion | tr '.p' '_0')

%define tmpArch %(echo %cmsplatf | cut -d_ -f 1,2)

%if "%{tmpArch}" == "slc3_ia32"
%define downloadarch i586
%endif

# A hack? Probably won't work for slc4 but...
%if "%{tmpArch}" == "slc4_ia32"
%define downloadarch i586
%endif

%if "%{tmpArch}" == "slc3_amd64"
%define downloadarch amd64
%endif

%if "%{tmpArch}" == "slc4_amd64"
%define downloadarch amd64
%endif

%if "%{tmpArch}" == "slc5_amd64"
%define downloadarch amd64
%endif

%if "%{tmpArch}" == "slc6_amd64"
%define downloadarch amd64
%endif

Source0: http://cmsrep.cern.ch/cmssw/jdk-mirror/jdk-%downloadv-linux-i586.bin
Source1: http://cmsrep.cern.ch/cmssw/jdk-mirror/jdk-%downloadv-linux-amd64.bin
%endif

%prep
%ifnos darwin
%define javadir jdk%(echo %realversion| sed -e "s/.p/_0/")
rm -rf %javadir
yes | sh %{_sourcedir}/jdk-%downloadv-linux-%downloadarch.bin
cd %javadir
%endif

%build

%install
%ifnos darwin
cp -r %javadir/* %i
rm -rf %i/man
%endif
