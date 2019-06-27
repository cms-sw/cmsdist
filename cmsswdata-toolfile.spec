### RPM cms cmsswdata-toolfile 3.0
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

for toolbase in `echo %pkgreqs | tr ' ' '\n' | grep 'cms/data-'` ; do
  toolver=`basename $toolbase`
  pack=`echo $toolbase | cut -d/ -f2 | sed 's|data-||;s|-|/|'`
  echo "      <flags CMSSW_DATA_PACKAGE=\"$pack=$toolver\"/>" >> %i/etc/scram.d/cmsswdata.xml
  echo "    <runtime name=\"CMSSW_SEARCH_PATH\" default=\"%{cmsroot}/%{cmsplatf}/$toolbase\" type=\"path\"/>" >> %i/searchpath.xml
done

cat %i/searchpath.xml >> %i/etc/scram.d/cmsswdata.xml
echo "  </tool>"      >> %i/etc/scram.d/cmsswdata.xml
rm -f %i/searchpath.xml

## IMPORT scram-tools-post
# bla bla
