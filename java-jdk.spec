### RPM external java-jdk 1.5.0.p6
## BUILDIF [ $(uname) != Darwin ]
%define downloadv %(echo %v | tr '.p' '_0')
Source: http://eulisse.web.cern.ch/eulisse/jdk-%downloadv-linux-i586.bin
%prep
ls
%define javadir jdk%(echo %v| sed -e "s/.p/_0/")
rm -rf %javadir
yes | sh %{_sourcedir}/jdk-%downloadv-linux-i586.bin
cd %javadir
%build
%install
ls 
cp -r %javadir/* %i
