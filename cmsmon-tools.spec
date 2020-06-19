### RPM cms cmsmon-tools 0.4.4
## NOCOMPILER

%define arch linux-amd64
%define promv 2.18.1
%define amver 0.20.0
%define pkg CMSMonitoring
%define ver %realversion
%define monit_commands monit ggus_parser
%define cmsmon_commands nats-sub nats-pub nats-exitcodes-termui dbs_vm
%define flags -ldflags="-s -w -extldflags -static" -p %{compiling_processes}
Source0: https://github.com/dmwm/%pkg/archive/%ver.tar.gz
Source1: https://github.com/prometheus/prometheus/releases/download/v%promv/prometheus-%promv.linux-amd64.tar.gz
Source2: https://github.com/prometheus/alertmanager/releases/download/v%amver/alertmanager-%amver.linux-amd64.tar.gz
Source3: https://github.com/vkuznet/hey/archive/x509-csv-fixes.tar.gz

BuildRequires: go

# RPM macros documentation
# http://www.rpm.org/max-rpm/s1-rpm-inside-macros.html
%prep
%setup -D -T -b 0 -n %pkg-%ver
%setup -D -T -b 1 -n prometheus-%promv.%arch
%setup -D -T -b 2 -n alertmanager-%amver.%arch
%setup -D -T -b 3 -n hey-x509-csv-fixes

%build
cd ../%pkg-%ver
mkdir -p gopath/bin
export GOPATH=$PWD/gopath
export GOCACHE=%{_builddir}/gocache
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
go get github.com/gizak/termui/v3

# build monit tools
pushd src/go/MONIT
  for cmd in %monit_commands; do
    go build %flags $cmd.go
  done
popd

# build NATS tools
pushd src/go/NATS
  for cmd in %cmsmon_commands; do
    go build %flags $cmd.go
  done
popd

# build hey tool
cd ../hey-x509-csv-fixes
go get github.com/vkuznet/hey/requester
make

%install
cd ../%pkg-%ver
for cmd in %monit_commands; do
  cp src/go/MONIT/$cmd %i/
done
for cmd in %cmsmon_commands; do
  cp src/go/NATS/$cmd %i/
done
# add prometheus, alertmanager tools to our install area
cd ../prometheus-%promv.%arch
cp promtool %i/
cp prometheus %i/
cd ../alertmanager-%amver.%arch
cp amtool %i/

# build hey tool
cd ../hey-x509-csv-fixes
cp hey %i
cd -

#####################################################
# **************** IMPORTANT NOTE ***************** #
# Increament cmsdist file revision for every change #
# This makes sure that latest revision is installed #
#####################################################
cat << \EOF > %i/.cmsmon-tools
#!/bin/bash -e
#CMSDIST_FILE_REVISION=1
eval $(scram unsetenv -sh)
THISDIR=$(dirname $0)
SHARED_ARCH=$(cmsos)
CMD=$(basename $0)
LATEST_VERSION=$(ls -d ${THISDIR}/../${SHARED_ARCH}_*/%{pkgcategory}/%{pkgname}/*/$CMD 2>/dev/null | sed -e 's|.*/%{pkgcategory}/%{pkgname}/||;s|/.*||' | sort | tail -1)
[ -z $LATEST_VERSION ] && >&2 echo "ERROR: Unable to find command '$CMD' for '$SHARED_ARCH' architecture." && exit 1
TOOL=$(ls -d ${THISDIR}/../${SHARED_ARCH}_*/%{pkgcategory}/%{pkgname}/${LATEST_VERSION}/$CMD 2>/dev/null | sort | tail -1)
$TOOL "$@"
EOF
chmod +x %i/.cmsmon-tools

%post
mkdir -p $RPM_INSTALL_PREFIX/cmsmon
%common_revision_script ${RPM_INSTALL_PREFIX}/%{pkgrel}/.cmsmon-tools $RPM_INSTALL_PREFIX/cmsmon/.cmsmon-tools
for cmd in %monit_commands %cmsmon_commands promtool amtool prometheus hey; do
  ln -sf .cmsmon-tools $RPM_INSTALL_PREFIX/cmsmon/$cmd
done
