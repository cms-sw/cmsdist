### RPM external geant4data 2.0
## NOCOMPILER

Requires: geant4-G4NDL
Requires: geant4-G4EMLOW
Requires: geant4-G4PhotonEvaporation
Requires: geant4-G4RadioactiveDecay
Requires: geant4-G4NEUTRONXS
Requires: geant4-G4SAIDDATA
Requires: geant4-G4ABLA
Requires: geant4-G4ENSDFSTATE

%prep
%build
%install
%post
if [ "X$CMS_INSTALL_PREFIX" = "X" ] ; then CMS_INSTALL_PREFIX=$RPM_INSTALL_PREFIX; export CMS_INSTALL_PREFIX; fi
echo "GEANT4DATA_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "set GEANT4DATA_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh
echo "GEANT4DATA_VERSION='%v'" >> $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "set GEANT4DATA_VERSION='%v'" >> $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh
# bla bla
