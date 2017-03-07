### RPM cms dasgoclient v00.00.04
## NOCOMPILER
%define dasgoclient_arch     slc6_amd64_gcc530
%define dasgoclient_pkg      cms+%{n}-binary+%{realversion}
%define dasgoclient_rpm      %{dasgoclient_pkg}-1-1.%{dasgoclient_arch}.rpm
Source0: http://cmsrep.cern.ch/cgi-bin/repos/cms/%{dasgoclient_arch}/%{dasgoclient_rpm}

%prep
%build
rpm2cpio %{_sourcedir}/%{dasgoclient_rpm} | cpio -idmv

%install
mkdir %{i}/etc
cp -r ./opt/cmssw/%{dasgoclient_arch}/$(echo %{dasgoclient_pkg} | tr '+' '/')/bin %{i}/bin
cat << \EOF > %{i}/etc/dasgoclient
#!/bin/sh
# VERSION:%{cmsplatf}/%{v}
# Clean-up CMSSW environment
if [ -f %{instroot}/common/scram ] ; then
  eval `%{instroot}/common/scram unsetenv -sh`
fi
# Sourcing dasclient environment
SHARED_ARCH=`%{instroot}/common/cmsos`
LATEST_VERSION=`cd %{instroot}; ls ${SHARED_ARCH}_*/%{pkgcategory}/%{pkgname}/v*/etc/profile.d/init.sh | sed 's|.*/%{pkgcategory}/%{pkgname}/||' | sort | tail -1`
DASGOCLIENT_ROOT=`ls %{instroot}/${SHARED_ARCH}_*/%{pkgcategory}/%{pkgname}/${LATEST_VERSION} | sort | tail -1 | sed 's|/etc/profile.d/init.sh$||'`
suffix="_linux"
case `uname -s` in
  Linux )
    case `uname -m` in
      aarch64 ) suffix="_arm64" ;;
      ppc64* )  suffix="_power8" ;;
      * )       suffix="_linux" ;;
    esac
  ;;
  Darwin )  suffix="_osx" ;;
esac
$DASGOCLIENT_ROOT/bin/dasgoclient${suffix} "$@"
EOF

chmod +x %i/etc/dasgoclient

%post
%{relocateConfig}etc/dasgoclient

# copy wrapper script into common if latest version is same as this version
mkdir -p $RPM_INSTALL_PREFIX/common
if [ "`ls ${RPM_INSTALL_PREFIX}/*/%{pkgcategory}/%{pkgname}/v*/etc/profile.d/init.sh | sed 's|.*/%{pkgcategory}/%{pkgname}/||;s|/etc/profile.d/init.sh||' | sort | tail -1`" = "%v" ] ; then
  /bin/cp -f ${RPM_INSTALL_PREFIX}/%{pkgrel}/etc/dasgoclient $RPM_INSTALL_PREFIX/common/dasgoclient.tmp
  mv $RPM_INSTALL_PREFIX/common/dasgoclient.tmp $RPM_INSTALL_PREFIX/common/dasgoclient
fi
