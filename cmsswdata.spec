### RPM cms cmsswdata 29
## NOCOMPILER
Source: none

%define BaseTool %(echo %n | tr '[a-z-]' '[A-Z_]')

%define isnotonline %(case %{cmsplatf} in (*onl_*_*) echo 0 ;; (*) echo 1 ;; esac)
%define isnotarmv7 %(case %{cmsplatf} in (*armv7*) echo 0 ;; (*) echo 1 ;; esac)

Requires: data-DetectorDescription-Schema
Requires: data-MagneticField-Interpolation
Requires: data-L1Trigger-L1TCalorimeter
Requires: data-L1Trigger-RPCTrigger
Requires: data-RecoParticleFlow-PFBlockProducer
Requires: data-RecoParticleFlow-PFTracking
Requires: data-RecoParticleFlow-PFProducer
Requires: data-RecoMuon-MuonIdentification
Requires: data-RecoMET-METPUSubtraction
Requires: data-RecoEgamma-ElectronIdentification
Requires: data-RecoEgamma-PhotonIdentification
Requires: data-RecoJets-JetProducers
Requires: data-CalibTracker-SiPixelESProducers
Requires: data-CalibCalorimetry-CaloMiscalibTools
Requires: data-Configuration-Generator
Requires: data-DQM-PhysicsHWW
Requires: data-CondFormats-JetMETObjects
Requires: data-RecoLocalCalo-EcalDeadChannelRecoveryAlgos
Requires: data-RecoHI-HiJetAlgos
Requires: data-GeneratorInterface-EvtGenInterface
Requires: data-MagneticField-Interpolation
Requires: data-RecoBTag-SoftLepton
Requires: data-Calibration-Tools
Requires: data-RecoBTag-SecondaryVertex
Requires: data-HLTrigger-JetMET
Requires: data-EventFilter-L1TRawToDigi
Requires: data-FastSimulation-TrackingRecHitProducer
Requires: data-RecoBTag-Combined
Requires: data-RecoBTag-CTagging
Requires: data-L1Trigger-L1TMuon
Requires: data-L1Trigger-L1TGlobal
Requires: data-L1Trigger-L1THGCal
Requires: data-SLHCUpgradeSimulations-Geometry

%if %isnotonline
# extra data dependencies for standard builds
Requires: data-FastSimulation-MaterialEffects
Requires: data-SimG4CMS-Calo
Requires: data-SimG4CMS-Forward
Requires: data-Validation-Geometry
Requires: data-Fireworks-Geometry
Requires: data-GeneratorInterface-ReggeGribovPartonMCInterface
%endif

%prep

%build

%install

%post
echo "%{BaseTool}_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "set %{BaseTool}_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh

for DATA_PATH in %directpkgreqs; do
  SOURCE=$RPM_INSTALL_PREFIX/%{cmsplatf}/$DATA_PATH
  PKG_DATA=$(ls $SOURCE | grep -v etc*)
  if [ -d $SOURCE/$PKG_DATA ] ; then
    echo "Moving $DATA_PATH in $SHARED"
    mkdir -p $RPM_INSTALL_PREFIX/share/$DATA_PATH/$PKG_DATA
    rsync -a --no-t --size-only $SOURCE/$PKG_DATA/ $RPM_INSTALL_PREFIX/share/$DATA_PATH/$PKG_DATA/ && rm -rf $SOURCE/$PKG_DATA && ln -fs ../../../../share/$DATA_PATH/$PKG_DATA $SOURCE/$PKG_DATA
  fi
done

