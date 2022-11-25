############## IMPORTANT #################
#For new dasgoclient_tag, set the version_suffix to 00
#For any other change, increment version_suffix
##########################################
%define version_suffix 00
%define dasgoclient_tag v02.04.49
### RPM cms crab-dev %{dasgoclient_tag}.rev%{version_suffix}
## NOCOMPILER
## NO_VERSION_SUFFIX

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
