### RPM cms exporters 0.0.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

%define pkg cmsweb-exporters
%define ver %realversion
Source0: https://github.com/vkuznet/%pkg/archive/%ver.tar.gz

Requires: go rotatelogs

# RPM macros documentation
# http://www.rpm.org/max-rpm/s1-rpm-inside-macros.html
%prep
%setup -D -T -b 0 -n %pkg-%ver

%build
cd ..
mkdir -p gopath
export GOPATH=$PWD/gopath
# build exporters
cd %pkg-%ver
go get github.com/dmwm/cmsauth
go get github.com/vkuznet/x509proxy
go get github.com/sirupsen/logrus
go get github.com/Lusitaniae/apache_exporter
go get github.com/prometheus/client_golang/prometheus
go get github.com/prometheus/common/log
go get github.com/prometheus/common/version

go build process_exporter.go
go build das2go_exporter.go
go build reqmgr_exporter.go
go build wmcore_exporter.go

wdir=$PWD

# build apache exporter
cd $GOPATH/src/github.com/Lusitaniae/apache_exporter
make build
cp apache_exporter $wdir

cd $wdir
echo $wdir
ls -al

%install
mkdir %i/bin
export GOPATH=$PWD/gopath
cp process_monitor.sh *_exporter %i/bin

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
%addDependency

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc
