### RPM cms dasgoclient v02.04.35
## NOCOMPILER
Source0: https://github.com/dmwm/dasgoclient/releases/download/%{realversion}/dasgoclient_amd64
Source1: https://github.com/dmwm/dasgoclient/releases/download/%{realversion}/dasgoclient_aarch64
Source2: https://github.com/dmwm/dasgoclient/releases/download/%{realversion}/dasgoclient_ppc64le

%prep
%build
%install
mkdir %{i}/etc %{i}/bin
cat << \EOF > %{i}/etc/dasgoclient
#!/bin/sh
# VERSION:%{cmsplatf}/%{v}
# Clean-up CMSSW environment
if [ -f %{instroot}/common/scram ] ; then
  eval `%{instroot}/common/scram unsetenv -sh`
fi
# Sourcing dasclient environment
SHARED_ARCH=`%{instroot}/common/cmsos`
LATEST_VERSION=`cd %{instroot}; ls ${SHARED_ARCH}_*/%{pkgcategory}/%{pkgname}/v*/bin/dasgoclient | sed 's|.*/%{pkgcategory}/%{pkgname}/||' | sort | tail -1`
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
if [ "`ls ${RPM_INSTALL_PREFIX}/*/%{pkgcategory}/%{pkgname}/v*/etc/profile.d/init.sh | sed 's|.*/%{pkgcategory}/%{pkgname}/||;s|/etc/profile.d/init.sh||' | sort | tail -1`" = "%v" ] ; then
  /bin/cp -f ${RPM_INSTALL_PREFIX}/%{pkgrel}/etc/dasgoclient $RPM_INSTALL_PREFIX/common/dasgoclient.tmp
  mv $RPM_INSTALL_PREFIX/common/dasgoclient.tmp $RPM_INSTALL_PREFIX/common/dasgoclient
fi

# make das_client point to dasgoclient in overrides/bin area
mkdir -p $RPM_INSTALL_PREFIX/share/overrides/bin
[ -e $RPM_INSTALL_PREFIX/share/overrides/bin/das_client ] || ln -sf ../../../common/dasgoclient $RPM_INSTALL_PREFIX/share/overrides/bin/das_client
