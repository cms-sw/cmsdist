### RPM cms data-FWCore-Framework V00-00-01

Source0: http://davidlt.web.cern.ch/davidlt/vault/cond_dump.root

%prep
# NOP

%build
# NOP

%install
DATADIR=%{i}/FWCore/Framework/data
mkdir -p ${DATADIR}
cp %{SOURCE0} ${DATADIR}
find %{i} -type d -exec chmod 0755 {} \;
find %{i} -type f -exec chmod 0644 {} \;

%post
%define base_tool %(echo "%{n}" | tr '[a-z-]' '[A-Z_]')
echo "%{base_tool}_ROOT='${CMS_INSTALL_PREFIX}/%{pkgrel}'" > ${RPM_INSTALL_PREFIX}/%{pkgrel}/etc/profile.d/init.sh
echo "set %{base_tool}_ROOT='${CMS_INSTALL_PREFIX}/%{pkgrel}'" > ${RPM_INSTALL_PREFIX}/%{pkgrel}/etc/profile.d/init.csh
