### RPM external geant4data-toolfile 1.0
Requires: geant4data

%prep
%build
%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/geant4data.xml
<tool name="geant4data" version="%v">
  <client>
    <environment name="GEANT4DATA_BASE" default="%{instroot}/%{cmsplatf}/%{pkgcategory}"/>
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

## IMPORT scram-tools-post
# bla bla
