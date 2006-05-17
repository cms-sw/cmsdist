### RPM external java-jdk 1.5.0.p6
## BUILDIF [ $(uname) != Darwin ]
%define downloadv %(echo %v | tr '.p' '_0')

%define tmpArch %(echo %cmsplatf | cut -d_ -f 1,2)

%if "%{tmpArch}" == "slc3_ia32"
%define downloadarch i586
%endif

%if "%{tmpArch}" == "slc3_amd64"
%define downloadarch amd64
%endif

%if "%{?downloadarch:set}" != "set"
%error Unsupported architecture.
%endif

Source: http://eulisse.web.cern.ch/eulisse/jdk-%downloadv-linux-%downloadarch.bin
%prep
ls
%define javadir jdk%(echo %v| sed -e "s/.p/_0/")
rm -rf %javadir
yes | sh %{_sourcedir}/jdk-%downloadv-linux-%downloadarch.bin
cd %javadir
%build
%install
ls 
cp -r %javadir/* %i
