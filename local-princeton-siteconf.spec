### RPM cms local-princeton-siteconf 1.0
## NOCOMPILER

%prep
# NOP

%build
# NOP

%install
mkdir -p %{i}/SITECONF/T3_US_Princeton_ARM/{JobConfig,PhEDEx}
ln -s T3_US_Princeton_ARM %{i}/SITECONF/local

cat <<XMLEOF > %{i}/SITECONF/T3_US_Princeton_ARM/JobConfig/site-local-config.xml
<site-local-config>
 <site name="T3_US_Princeton_ARM">
    <event-data>
      <catalog url="trivialcatalog_file:%{i}/SITECONF/local/PhEDEx/storage.xml?protocol=xrootd"/>
    </event-data>
    <source-config>
        <cache-hint value="storage-only"/>
        <read-hint value="read-ahead-buffered"/>
        <ttree-cache-size value="33554432"/>
    </source-config>
    <calib-data>
     <frontier-connect>
       <failover toserver="no"/>
       <load balance="proxies"/>
       <proxy url="http://della.princeton.edu:3128"/>
       <server url="http://cmsfrontier.cern.ch:8000/FrontierInt"/>
       <server url="http://cmsfrontier1.cern.ch:8000/FrontierInt"/>
       <server url="http://cmsfrontier2.cern.ch:8000/FrontierInt"/>
       <server url="http://cmsfrontier3.cern.ch:8000/FrontierInt"/>
     </frontier-connect>
    </calib-data>
 </site>
 </site-local-config>
XMLEOF

cat <<XMLEOF > %{i}/SITECONF/T3_US_Princeton_ARM/PhEDEx/storage.xml
<storage-mapping>
  <lfn-to-pfn
    protocol="xrootd"
    destination-match=".*"
    path-match="/+store/(.*)"
    result="root://xrootd.unl.edu//store/\$1?source=non_cms"/>

  <lfn-to-pfn
    protocol="direct"
    path-match="/+store/(.*)"
    result="/cms/store/$1"/>
</storage-mapping>
XMLEOF

%post
%{relocateConfig}/SITECONF/T3_US_Princeton_ARM/JobConfig/site-local-config.xml
if [ ! -d $RPM_INSTALL_PREFIX/SITECONF ] ; then 
  rm -f $RPM_INSTALL_PREFIX/SITECONF
  ln -s %{pkgrel}/SITECONF $RPM_INSTALL_PREFIX/SITECONF
fi
# bla bla
