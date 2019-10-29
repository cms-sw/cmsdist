### RPM cms cmsswdata 36
## NOCOMPILER
Source: none

%define BaseTool %(echo %n | tr '[a-z-]' '[A-Z_]')

%define isnotonline %(case %{cmsplatf} in (*onl_*_*) echo 0 ;; (*) echo 1 ;; esac)
%define isnotarmv7 %(case %{cmsplatf} in (*armv7*) echo 0 ;; (*) echo 1 ;; esac)

Requires: data-CondTools-SiPhase2Tracker
Requires: data-PhysicsTools-PatUtils
Requires: data-RecoTauTag-TrainingFiles
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
Requires: data-CalibPPS-ESProducers
Requires: data-Configuration-Generator
Requires: data-DQM-PhysicsHWW
Requires: data-DQM-SiStripMonitorClient
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
Requires: data-CalibTracker-SiStripDCS
Requires: data-SimTracker-SiStripDigitizer
Requires: data-CalibCalorimetry-EcalTrivialCondModules
Requires: data-DataFormats-PatCandidates
Requires: data-SimTransport-HectorProducer
Requires: data-PhysicsTools-NanoAOD
Requires: data-RecoTracker-FinalTrackSelectors
Requires: data-EgammaAnalysis-ElectronTools
Requires: data-DQM-DTMonitorClient
Requires: data-SimTransport-PPSProtonTransport
Requires: data-SimTransport-TotemRPProtonTransportParametrization
Requires: data-FWCore-Modules
Requires: data-IOPool-Input
Requires: data-RecoCTPPS-TotemRPLocal
Requires: data-IOPool-Input
Requires: data-RecoHGCal-TICL
Requires: data-SimG4CMS-HGCalTestBeam
Requires: data-SimPPS-PPSPixelDigiProducer

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
  PKG_DIR=$(echo $DATA_PATH | cut -d/ -f2)
  [ $(echo $PKG_DIR | grep '^data-' | wc -l) -eq 1 ] || continue
  PKG_DIR=$(echo $PKG_DIR | sed 's|^data-||;s|-|/|')
  SOURCE=$RPM_INSTALL_PREFIX/%{cmsplatf}/$DATA_PATH
  PKG_DATA=$(echo $PKG_DIR | cut -d/ -f1)
  if [ ! -e $RPM_INSTALL_PREFIX/share/$DATA_PATH/$PKG_DIR ] ; then
    rm -rf $RPM_INSTALL_PREFIX/share/$DATA_PATH
    mkdir -p $RPM_INSTALL_PREFIX/share/$DATA_PATH
    if [ -L $SOURCE/$PKG_DATA ] ; then
      ln -fs ../../../../%{cmsplatf}/$DATA_PATH/$PKG_DATA $RPM_INSTALL_PREFIX/share/$DATA_PATH/$PKG_DATA
    else
      echo "Moving $DATA_PATH in share"
      rsync -aq --no-t --size-only $SOURCE/$PKG_DATA/ $RPM_INSTALL_PREFIX/share/$DATA_PATH/$PKG_DATA/
    fi
  fi
  if [ ! -L $SOURCE/$PKG_DATA ] ; then
    rm -rf $SOURCE/$PKG_DATA && ln -fs ../../../../share/$DATA_PATH/$PKG_DATA $SOURCE/$PKG_DATA
  fi
done
