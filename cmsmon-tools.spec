### RPM cms cmsmon-tools 0.5.27
## NOCOMPILER

%define arch linux-amd64
%define promv 2.25.1
%define amver 0.21.0
%define sternv 1.11.0
%define apsver 0.1.85
%define monit_commands monit ggus_parser alert annotationManager nats-sub nats-pub dbs_vm
%define common_commands promtool amtool prometheus hey stern
%define flags -ldflags="-s -w -extldflags -static" -p %{compiling_processes}
Source0: https://github.com/dmwm/CMSMonitoring/releases/download/%{realversion}/cmsmon-tools.tar.gz
Source1: https://github.com/prometheus/prometheus/releases/download/v%promv/prometheus-%promv.linux-amd64.tar.gz
Source2: https://github.com/prometheus/alertmanager/releases/download/v%amver/alertmanager-%amver.linux-amd64.tar.gz
Source3: https://github.com/vkuznet/hey/archive/x509-csv-fixes.tar.gz
Source4: https://github.com/wercker/stern/releases/download/%sternv/stern_linux_amd64
Source5: https://github.com/vkuznet/auth-proxy-server/releases/download/%apsver/auth-proxy-tools.tar.gz

BuildRequires: go

# RPM macros documentation
# http://www.rpm.org/max-rpm/s1-rpm-inside-macros.html
%prep
%setup -D -T -b 0 -n cmsmon-tools
%setup -D -T -b 1 -n prometheus-%promv.%arch
%setup -D -T -b 3 -n hey-x509-csv-fixes
%setup -D -T -b 2 -n alertmanager-%amver.%arch
%setup -D -T -b 5 -n auth-proxy-tools

%build
mkdir -p gopath/bin
export GOPATH=$PWD/gopath
export GOCACHE=%{_builddir}/gocache
go get github.com/dmwm/cmsauth
go get github.com/vkuznet/x509proxy

# build hey tool
cd %{_builddir}/hey-x509-csv-fixes
go get github.com/vkuznet/hey/requester
make

%install
cd %{_builddir}/cmsmon-tools
# copy CMS monitoring tools
for cmd in %monit_commands; do
    cp $cmd %i/
done
# add prometheus, alertmanager tools to our install area
cd %{_builddir}/prometheus-%promv.%arch
cp promtool %i/
cp prometheus %i/
cd %{_builddir}/alertmanager-%amver.%arch
cp amtool %i/

# build hey tool
cd %{_builddir}/hey-x509-csv-fixes
cp hey %i
cd -

# install stern
cp %{_sourcedir}/stern_linux_amd64 %i/stern
chmod +x %i/stern

# install token-manager
cd %{_builddir}/auth-proxy-tools
cp token-manager %i/
cp auth-token %i/
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
chmod -R u+w %{_builddir}/hey-x509-csv-fixes
rm -rf %{_builddir}/hey-x509-csv-fixes

%post
mkdir -p $RPM_INSTALL_PREFIX/cmsmon
%common_revision_script ${RPM_INSTALL_PREFIX}/%{pkgrel}/.cmsmon-tools $RPM_INSTALL_PREFIX/cmsmon/.cmsmon-tools
for cmd in %monit_commands %cmsmon_commands %common_commands; do
  ln -sf .cmsmon-tools $RPM_INSTALL_PREFIX/cmsmon/$cmd
done
