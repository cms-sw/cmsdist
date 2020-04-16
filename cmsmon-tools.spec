### RPM cms cmsmon-tools 0.3.8
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

%define pkg CMSMonitoring
%define ver %realversion
Source0: https://github.com/dmwm/%pkg/archive/%ver.tar.gz

#Requires: go

# RPM macros documentation
# http://www.rpm.org/max-rpm/s1-rpm-inside-macros.html
%prep
%setup -D -T -b 0 -n %pkg-%ver

%build
cd ..
cd %pkg-%ver
echo "build $PWD"
ls
mkdir -p gopath/bin
export GOPATH=$PWD/gopath
go get github.com/dmwm/cmsauth
go get github.com/vkuznet/x509proxy
go get github.com/sirupsen/logrus
go get github.com/prometheus/client_golang/prometheus
go get github.com/prometheus/common/log
go get github.com/prometheus/common/version
go get github.com/shirou/gopsutil/cpu
go get github.com/shirou/gopsutil/mem
go get github.com/shirou/gopsutil/load
go get github.com/shirou/gopsutil/process
go get github.com/go-stomp/stomp
go get github.com/nats-io/nats.go

# build monit tools
cd src/go/MONIT
go build monit.go
cd -
# build NATS tools
cd src/go/NATS
go build nats-sub.go
cd -

%install
cd ../%pkg-%ver
echo "### current dir: $PWD"
cp src/go/MONIT/monit %i/
cp src/go/NATS/nats-sub %i/

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
%addDependency

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

%files
%{installroot}/%{pkgrel}/monit
%{installroot}/%{pkgrel}/nats-sub
