### RPM cms exporters 0.0.11
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

%define pkg cmsweb-exporters
%define ver %realversion
%define pkg1 glide
%define ver1 0.13.2
%define dir1 linux-amd64
%define pkg2 mongodb_exporter
%define ver2 1.0.0
Source0: https://github.com/vkuznet/%pkg/archive/%ver.tar.gz
Source1: https://github.com/Masterminds/%pkg1/releases/download/v%ver1/%pkg1-v%ver1-linux-amd64.tar.gz
Source2: https://github.com/dcu/%pkg2/archive/v%ver2.tar.gz

Requires: go rotatelogs

# RPM macros documentation
# http://www.rpm.org/max-rpm/s1-rpm-inside-macros.html
%prep
%setup -D -T -b 0 -n %pkg-%ver
# glide tar ball provides linux-amd64 directory
%setup -D -T -b 1 -n %dir1
%setup -D -T -b 2 -n %pkg2-%ver2
echo "### prep: $PWD"

%build
cd ..
mkdir -p gopath/bin
export GOPATH=$PWD/gopath
# copy glide and mongo
export PATH=$PATH:$GOPATH/bin
cp %dir1/glide $GOPATH/bin
mkdir -p $GOPATH/src/github.com/dcu/
cp -r %pkg2-%ver2 $GOPATH/src/github.com/dcu/mongodb_exporter

# build exporters
cd %pkg-%ver
go get github.com/dmwm/cmsauth
go get github.com/vkuznet/x509proxy
go get github.com/sirupsen/logrus
go get github.com/Lusitaniae/apache_exporter
go get github.com/prometheus/client_golang/prometheus
go get github.com/prometheus/common/log
go get github.com/prometheus/common/version
go get github.com/shirou/gopsutil/cpu
go get github.com/shirou/gopsutil/mem
go get github.com/shirou/gopsutil/load
go get github.com/shirou/gopsutil/process
go get github.com/golang/dep/cmd/dep
go get github.com/golang/glog
go get github.com/namsral/flag
go get github.com/gesellix/couchdb-prometheus-exporter/glogadapt
go get github.com/gesellix/couchdb-prometheus-exporter/lib
go get github.com/gesellix/couchdb-prometheus-exporter
go get github.com/prometheus/node_exporter

go build process_exporter.go
go build das2go_exporter.go
go build reqmgr_exporter.go
go build wmcore_exporter.go

wdir=$PWD

# build apache exporter
cd $GOPATH/src/github.com/Lusitaniae/apache_exporter
make build
cp apache_exporter $wdir

# build couchdb exporter
cd $GOPATH/src/github.com/gesellix/couchdb-prometheus-exporter
go build -o couchdb_exporter
cp couchdb_exporter $wdir

# build mongodb exporter
cd $GOPATH/src/github.com/dcu/mongodb_exporter
make build
cp mongodb_exporter $wdir

# build node exporter
cd ${GOPATH-$HOME/go}/src/github.com/prometheus/node_exporter
make
cp node_exporter $wdir

cd $wdir
echo "### build dir: $wdir"

%install
mkdir %i/bin
export GOPATH=$PWD/gopath
cd ../%pkg-%ver
echo "### current dir: $PWD"
cp process_monitor.sh *_exporter %i/bin

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
%addDependency

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc
