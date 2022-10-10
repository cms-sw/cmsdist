### RPM external geant4data 11.0
## NOCOMPILER

Requires: geant4-G4NDL
Requires: geant4-G4EMLOW
Requires: geant4-G4PhotonEvaporation
Requires: geant4-G4RadioactiveDecay
Requires: geant4-G4PARTICLEXS
Requires: geant4-G4SAIDDATA
Requires: geant4-G4ABLA
Requires: geant4-G4ENSDFSTATE
Requires: geant4-G4RealSurface
Requires: geant4-G4INCL

%prep
%build
%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/geant4data.xml
<tool name="geant4data" version="%v">
  <client>
    <environment name="GEANT4DATA_BASE" default="%{cmsroot}/%{cmsplatf}/%{pkgcategory}"/>
  </client>
EOF_TOOLFILE

for tool in `echo %requiredtools | tr ' ' '\n' | grep 'geant4-'` ; do
  uctool=`echo $tool | tr '-' '_' | tr '[a-z]' '[A-Z]'`
  toolbase=`eval echo \\$${uctool}_ROOT`
  toolenv=`eval echo \\$${uctool}_RUNTIME`
  echo "$uctool = $toolbase, $toolenv"
  if [ "X$toolbase" = X -o "X$toolenv" = X -o ! -d $toolbase/data ] ; then continue ; fi
  tooldata=`ls -d $toolbase/data/* | tail -1`
  if [ "X$tooldata" = X ] ; then continue ; fi
  echo "  <runtime name=\"$toolenv\" value=\"$tooldata\" type=\"path\"/>" >> %i/etc/scram.d/geant4data.xml
done
echo "</tool>" >> %i/etc/scram.d/geant4data.xml
chmod +r %i/etc/scram.d/geant4data.xml

%post
if [ "X$CMS_INSTALL_PREFIX" = "X" ] ; then CMS_INSTALL_PREFIX=$RPM_INSTALL_PREFIX; export CMS_INSTALL_PREFIX; fi
%{relocateConfig}etc/scram.d/*.xml
echo "GEANT4DATA_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "set GEANT4DATA_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh
echo "GEANT4DATA_VERSION='%v'" >> $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "set GEANT4DATA_VERSION='%v'" >> $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh

