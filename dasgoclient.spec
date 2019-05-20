### RPM cms dasgoclient v02.02.01
## NOCOMPILER
%define dasgoclient_arch     slc6_amd64_gcc700
%define dasgoclient_pkg      cms+%{n}-binary+%{realversion}
%define dasgoclient_rpm      %{dasgoclient_pkg}-1-1.%{dasgoclient_arch}.rpm
Source0: https://cern.ch/valya/dasgoclient/%{dasgoclient_rpm}

%prep
%build
rpm2cpio %{_sourcedir}/%{dasgoclient_rpm} | cpio -idmv

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

suffix="_linux"
case %{cmsos} in
  *_aarch64 ) suffix="_arm64"  ;;
  *_ppc64*  ) suffix="_power8" ;;
  osx*      ) suffix="_osx"    ;;
  *_amd64   ) suffix="_linux"  ;;
esac
cp -r ./opt/cmssw/%{dasgoclient_arch}/$(echo %{dasgoclient_pkg} | tr '+' '/')/bin/dasgoclient${suffix} %{i}/bin/dasgoclient
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
