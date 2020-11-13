### RPM cms cmsmon-tools 0.5.8
## NOCOMPILER

%define arch linux-amd64
%define promv 2.19.2
%define amver 0.21.0
%define sternv 1.11.0
%define monit_commands monit ggus_parser alert annotationManager nats-sub nats-pub nats-exitcodes-termui dbs_vm
%define common_commands promtool amtool prometheus hey stern
%define flags -ldflags="-s -w -extldflags -static" -p %{compiling_processes}
Source0: https://github.com/dmwm/CMSMonitoring/releases/download/%{realversion}/cmsmon-tools.tar.gz
Source1: https://github.com/prometheus/prometheus/releases/download/v%promv/prometheus-%promv.linux-amd64.tar.gz
Source2: https://github.com/prometheus/alertmanager/releases/download/v%amver/alertmanager-%amver.linux-amd64.tar.gz
Source3: https://github.com/vkuznet/hey/archive/x509-csv-fixes.tar.gz

BuildRequires: go

# RPM macros documentation
# http://www.rpm.org/max-rpm/s1-rpm-inside-macros.html
%prep
%setup -D -T -b 0 -n cmsmon-tools
%setup -D -T -b 1 -n prometheus-%promv.%arch
%setup -D -T -b 2 -n alertmanager-%amver.%arch
%setup -D -T -b 3 -n hey-x509-csv-fixes

%build
mkdir -p gopath/bin
export GOPATH=$PWD/gopath
export GOCACHE=%{_builddir}/gocache
go get github.com/dmwm/cmsauth
go get github.com/vkuznet/x509proxy

# build hey tool
cd ../hey-x509-csv-fixes
go get github.com/vkuznet/hey/requester
make

%install
cd ../cmsmon-tools
# copy CMS monitoring tools
for cmd in %monit_commands; do
    cp $cmd %i/
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

# install stern
cd ../
curl -ksLO https://github.com/wercker/stern/releases/download/%sternv/stern_linux_amd64
chmod +x stern_linux_amd64
cp stern_linux_amd64 %i/stern
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
for cmd in %monit_commands %cmsmon_commands %common_commands; do
  ln -sf .cmsmon-tools $RPM_INSTALL_PREFIX/cmsmon/$cmd
done
