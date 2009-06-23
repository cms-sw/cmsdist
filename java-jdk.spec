### RPM external java-jdk 1.5.0_15
## BUILDIF [ "$(uname)" != "Darwin" ]

Provides: libasound.so.2
Provides: libasound.so.2(ALSA_0.9) 
Provides: libjava_crw_demo_g.so 
Provides: libodbc.so 
Provides: libodbcinst.so

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

Source0: http://cmsrep.cern.ch/cmssw/jdk-mirror/jdk-%downloadv-linux-i586.bin
Source1: http://cmsrep.cern.ch/cmssw/jdk-mirror/jdk-%downloadv-linux-amd64.bin

%prep
%if %(uname) != Darwin
ls
%define javadir jdk%(echo %realversion| sed -e "s/.p/_0/")
rm -rf %javadir
yes | sh %{_sourcedir}/jdk-%downloadv-linux-%downloadarch.bin
cd %javadir
%endif
%build
%install
%if %(uname) != Darwin
ls 
cp -r %javadir/* %i
%endif
