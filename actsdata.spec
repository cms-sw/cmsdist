### RPM external actsdata v10
## NOCOMPILER

%define archive traccc-data-%{realversion}.tar.gz
Source: https://acts.web.cern.ch/traccc/data/%{archive} 

%prep

%build

%install
cp %{SOURCE0} %{i}/%{archive}

%post
LOCAL_PKG=${RPM_INSTALL_PREFIX}/%{pkgrel}
SHARE_PKG=${RPM_INSTALL_PREFIX}/share/%{pkgcategory}/%{n}/%{realversion}
if ! [ -d ${SHARE_PKG} ]; then
  mkdir -p ${SHARE_PKG}
  tar xvzf ${LOCAL_PKG}/%{archive} -C ${SHARE_PKG}
fi
rm -f ${LOCAL_PKG}/%{archive}
cd ${LOCAL_PKG}/
ln -s ../../../../share/%{pkgcategory}/%{n}/%{realversion}/* .
