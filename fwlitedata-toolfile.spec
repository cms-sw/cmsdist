### RPM cms fwlitedata-toolfile 1.0
Requires: fwlitedata
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/fwlitedata.xml
<tool name="fwlitedata" version="@TOOL_VERSION@">
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
  echo "<runtime name=\"CMSSW_SEARCH_PATH\" default=\"$toolbase\" handler=\"warn\" type=\"path\"/>" >> %i/etc/scram.d/fwlitedata.xml
done
echo "</tool>" >> %i/etc/scram.d/fwlitedata.xml

## IMPORT scram-tools-post
# bla bla
