### RPM cms cmsswdata 23
Source: none

%define closingbrace )
%define online %(case %cmsplatf in *onl_*_*%closingbrace echo true;; *%closingbrace echo false;; esac)

%if "%online" != "true"
# data dependencies for standard builds
Requires: data-FastSimulation-MaterialEffects
Requires: data-FastSimulation-PileUpProducer
Requires: data-MagneticField-Interpolation
Requires: data-RecoParticleFlow-PFBlockProducer
Requires: data-RecoParticleFlow-PFTracking
Requires: data-RecoParticleFlow-PFProducer
Requires: data-RecoTracker-RingESSource
Requires: data-RecoTracker-RoadMapESSource
Requires: data-SimG4CMS-Calo
Requires: data-Validation-Geometry
Requires: data-RecoMuon-MuonIdentification
Requires: data-L1Trigger-RPCTrigger
Requires: data-Fireworks-Geometry
%else
# data dependencies for ONLINE builds
Requires: data-MagneticField-Interpolation
%endif

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
  toolbase=`perl -e 'print "$ENV{'$uctool'_ROOT}\n";'`
  echo "$uctool = $toolbase"
  if [ "X$toolbase" = X -o ! -d $toolbase/etc ] ; then continue ; fi
  echo "<runtime name=\"CMSSW_SEARCH_PATH\" default=\"$toolbase\" handler=\"warn\" type=\"path\"/>" >> %i/etc/scram.d/%n.xml
done
echo "</tool>" >> %i/etc/scram.d/%n.xml

%post
%{relocateConfig}etc/scram.d/%n.xml
