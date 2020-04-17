### RPM cms cmsmon-tools 0.3.10
## NOCOMPILER

%define pkg CMSMonitoring
%define ver %realversion
%define cmsmon_commands nats-sub nats-pub nats-exitcodes-termui dbs_vm
%define flags -ldflags="-s -w -extldflags -static" -p %{compiling_processes}
Source0: https://github.com/dmwm/%pkg/archive/%ver.tar.gz

BuildRequires: go

# RPM macros documentation
# http://www.rpm.org/max-rpm/s1-rpm-inside-macros.html
%prep
%setup -D -T -b 0 -n %pkg-%ver

%build
export GOCACHE=%{_builddir}/gocache
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
go get github.com/gizak/termui/v3

# build monit tools
cd src/go/MONIT
go build %flags monit.go
cd -
# build NATS tools
cd src/go/NATS
for cmd in %cmsmon_commands; do
if [ -f $cmd.go ]; then
go build %flags $cmd.go
fi
done
cd -

%install
cd ../%pkg-%ver
echo "### current dir: $PWD"
cp src/go/MONIT/monit %i/
for cmd in %cmsmon_commands; do
if [ -f src/go/NATS/$cmd ]; then
cp src/go/NATS/$cmd %i/
fi
done

%post
mkdir -p $RPM_INSTALL_PREFIX/cmsmon
for cmd in %cmsmon_commands; do
cat << \EOF > $RPM_INSTALL_PREFIX/cmsmon/$cmd
#!/bin/bash -e
eval $(scram unsetenv -sh)
THISDIR=$(dirname \$0)
SHARED_ARCH=$(cmsos)
cmd=$(basename $0)
TOOL=$(ls -d ${THISDIR}/../${SHARED_ARCH}_*/cms/cmsmon-tools/*/$cmd 2>/dev/null | sort | tail -1)
[ -z $TOOL ] && >&2 echo "ERROR: Unable to find command '$cmd' for '$SHARED_ARCH' architecture." && exit 1
$TOOL "$@"
EOF
chmod +x $RPM_INSTALL_PREFIX/cmsmon/$cmd
done
