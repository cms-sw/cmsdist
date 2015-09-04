### RPM cms cmsswdata 28
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
