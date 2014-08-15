### RPM cms cmsswdata 27
## NOCOMPILER
Source: none

%define BaseTool %(echo %n | tr '[a-z-]' '[A-Z_]')

%define isnotonline %(case %{cmsplatf} in (*onl_*_*) echo 0 ;; (*) echo 1 ;; esac)
%define isnotarmv7 %(case %{cmsplatf} in (*armv7*) echo 0 ;; (*) echo 1 ;; esac)

Requires: data-DetectorDescription-Schema
Requires: data-MagneticField-Interpolation
Requires: data-Geometry-CMSCommonData
Requires: data-Geometry-CSCGeometryBuilder
Requires: data-Geometry-DTGeometryBuilder
Requires: data-Geometry-EcalCommonData
Requires: data-Geometry-EcalSimData
Requires: data-Geometry-EcalTestBeam
Requires: data-Geometry-FP420CommonData
Requires: data-Geometry-FP420SimData
Requires: data-Geometry-ForwardCommonData
Requires: data-Geometry-ForwardSimData
Requires: data-Geometry-HcalCommonData
Requires: data-Geometry-HcalSimData
Requires: data-Geometry-HcalTestBeamData
Requires: data-Geometry-MTCCTrackerCommonData
Requires: data-Geometry-MuonCommonData
Requires: data-Geometry-MuonSimData
Requires: data-Geometry-RPCGeometryBuilder
Requires: data-Geometry-TrackerCommonData
Requires: data-Geometry-TrackerRecoData
Requires: data-Geometry-TrackerSimData
Requires: data-Geometry-TwentyFivePercentTrackerCommonData
Requires: data-Geometry-CaloEventSetup
Requires: data-L1Trigger-RPCTrigger
Requires: data-RecoParticleFlow-PFBlockProducer
Requires: data-RecoParticleFlow-PFTracking
Requires: data-RecoParticleFlow-PFProducer
Requires: data-RecoMuon-MuonIdentification
Requires: data-RecoEgamma-ElectronIdentification
Requires: data-RecoJets-JetProducers
Requires: data-CalibTracker-SiPixelESProducers
Requires: data-CalibCalorimetry-CaloMiscalibTools
Requires: data-Configuration-Generator
Requires: data-DQM-PhysicsHWW
Requires: data-CondFormats-JetMETObjects
Requires: data-RecoLocalCalo-EcalDeadChannelRecoveryAlgos
Requires: data-RecoHI-HiJetAlgos

%if %isnotonline
# extra data dependencies for standard builds
Requires: data-FastSimulation-MaterialEffects
%if %isnotarmv7
Requires: data-FastSimulation-PileUpProducer
%endif
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
