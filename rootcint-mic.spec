### RPM lcg rootcint-mic 5.34.07
## NOCOMPILER
Source: http://cern.ch/muzaffar/%n-%{realversion}.tar.gz

%prep
%setup -n %n-%realversion

%build
%install
cp -r * %i/

%post
echo "ROOTCINT_MIC_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "ROOTCINT_MIC_VERSION='%v'" >> $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "set ROOTCINT_MIC_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh
echo "set ROOTCINT_MIC_VERSION='%v'" >> $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh
