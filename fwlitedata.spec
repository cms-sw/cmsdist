### RPM cms fwlitedata 25
## NOCOMPILER
Source: none

Requires: data-Fireworks-Geometry
Requires: data-DataFormats-PatCandidates

%prep
%build
%install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="%n" version="%v">
    <client>
      <environment name="CMSSWDATA_BASE" default="%{instroot}/%{cmsplatf}/%{pkgcategory}"/>
      <environment name="CMSSW_DATA_PATH" default="$CMSSWDATA_BASE"/>
    </client>
    <runtime name="CMSSW_DATA_PATH" value="$CMSSWDATA_BASE" handler="warn" type="path"/>
EOF_TOOLFILE
for tool in `echo %requiredtools | tr ' ' '\n' | grep 'data-'` ; do
  uctool=`echo $tool | tr '-' '_' | tr '[a-z]' '[A-Z]'`
  toolbase=`eval echo \\$${uctool}_ROOT`
  echo "$uctool = $toolbase"
  if [ "X$toolbase" = X -o ! -d $toolbase/etc ] ; then continue ; fi
  echo "<runtime name=\"CMSSW_SEARCH_PATH\" default=\"$toolbase\" handler=\"warn\" type=\"path\"/>" >> %i/etc/scram.d/%n.xml
done
echo "</tool>" >> %i/etc/scram.d/%n.xml

%post
%{relocateConfig}etc/scram.d/%n.xml
# bla bla
