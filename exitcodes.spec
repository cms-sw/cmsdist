### RPM cms exitcodes 0.0.2
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

%define repo github.com/vkuznet/CMSExitCodes
Source0: https://%repo/archive/v%realversion.tar.gz

Requires: go rotatelogs

# RPM macros documentation
# http://www.rpm.org/max-rpm/s1-rpm-inside-macros.html
%prep
%setup -D -T -b 0 -n CMSExitCodes-%realversion

%build
cd ..
mkdir -p gopath
export GOPATH=$PWD/gopath
go get github.com/sirupsen/logrus
go get -d github.com/shirou/gopsutil/...
go get %repo

%install
cd ..
export GOPATH=$PWD/gopath
cp $GOPATH/bin/CMSExitCodes %i/bin

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
%addDependency

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc
