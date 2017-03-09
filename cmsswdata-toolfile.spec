### RPM cms cmsswdata-toolfile 2.0
Requires: cmsswdata
%prep

%build

%install

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/cmsswdata.xml
  <tool name="cmsswdata" version="%v">
    <client>
      <environment name="CMSSWDATA_BASE" default="%{instroot}/%{cmsplatf}/%{pkgcategory}"/>
      <environment name="CMSSW_DATA_PATH" default="$CMSSWDATA_BASE"/>
EOF_TOOLFILE

cat << \EOF_TOOLFILE > %i/searchpath.xml
    </client>
    <runtime name="CMSSW_DATA_PATH" value="$CMSSWDATA_BASE" type="path"/>
EOF_TOOLFILE

for tool in `echo %requiredtools | tr ' ' '\n' | grep 'data-'` ; do
  uctool=`echo $tool | tr '-' '_' | tr '[a-z]' '[A-Z]'`
  toolbase=`eval echo \\$${uctool}_ROOT`
  if [ "X$toolbase" = X ] ; then exit 1 ; fi
  toolver=`basename $toolbase | sed 's|-cms[0-9]*||'`
  pack=`echo $tool | sed 's|data-||;s|-|/|'`
  echo "      <flags CMSSW_DATA_PACKAGE=\"$pack=$toolver\"/>" >> %i/etc/scram.d/cmsswdata.xml
  echo "    <runtime name=\"CMSSW_SEARCH_PATH\" default=\"$toolbase\" type=\"path\"/>" >> %i/searchpath.xml
done

cat %i/searchpath.xml >> %i/etc/scram.d/cmsswdata.xml
echo "  </tool>"      >> %i/etc/scram.d/cmsswdata.xml
rm -f %i/searchpath.xml

## IMPORT scram-tools-post
