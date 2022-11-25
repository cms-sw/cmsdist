### RPM cms dasgoclient v20221125.0
## NOCOMPILER
## NO_VERSION_SUFFIX
####### NOTE ########
# For any changes in this file (e.g. updating dasgoclient_tag or build recipe changes) please
# always use the latest date as version in first line
#####################
%define dasgoclient_tag v02.04.49
Source0: https://github.com/dmwm/dasgoclient/releases/download/%{dasgoclient_tag}/dasgoclient_amd64
Source1: https://github.com/dmwm/dasgoclient/releases/download/%{dasgoclient_tag}/dasgoclient_aarch64
Source2: https://github.com/dmwm/dasgoclient/releases/download/%{dasgoclient_tag}/dasgoclient_ppc64le

%prep
%build
%install
mkdir %{i}/etc %{i}/bin
cat << \EOF > %{i}/etc/dasgoclient
#!/bin/sh
# CMSDIST_FILE_REVISION=1
# Clean-up CMSSW environment
if [ -f %{instroot}/common/scram ] ; then
  eval `%{instroot}/common/scram unsetenv -sh`
fi
# Sourcing dasclient environment
SHARED_ARCH=`%{instroot}/common/cmsos`
[ $(ls %{instroot}/${SHARED_ARCH}_*/cms/dasgoclient 2>/dev/null | wc -l) -eq 0 ] && SHARED_ARCH=$(echo $SCRAM_ARCH | cut -d_ -f1,2)
LATEST_VERSION=`ls %{instroot}/${SHARED_ARCH}_*/%{pkgcategory}/%{pkgname}/v*/bin/dasgoclient | sed 's|.*/%{pkgcategory}/%{pkgname}/||' | sort | tail -1`
DASGOCLIENT=`ls %{instroot}/${SHARED_ARCH}_*/%{pkgcategory}/%{pkgname}/${LATEST_VERSION} | sort | tail -1`
$DASGOCLIENT "$@"
EOF

chmod +x %i/etc/dasgoclient
cp -pL %{_sourcedir}/dasgoclient_$(echo %{cmsplatf} | cut -d_ -f2) %{i}/bin/dasgoclient
chmod +x %{i}/bin/dasgoclient

%post
%{relocateConfig}etc/dasgoclient

# copy wrapper script into common if latest version is same as this version
mkdir -p $RPM_INSTALL_PREFIX/common
%common_revision_script ${RPM_INSTALL_PREFIX}/%{pkgrel}/etc/dasgoclien $RPM_INSTALL_PREFIX/common/dasgoclient

# make das_client point to dasgoclient in overrides/bin area
mkdir -p $RPM_INSTALL_PREFIX/share/overrides/bin
[ -e $RPM_INSTALL_PREFIX/share/overrides/bin/das_client ] || ln -sf ../../../common/dasgoclient $RPM_INSTALL_PREFIX/share/overrides/bin/das_client
