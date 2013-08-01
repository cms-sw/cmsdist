### RPM cms data-RecoParticleFlow-PFBlockProducer V02-04-02

%prep

# Base URL, where to find the files
%define base_url "http://cmsdoc.cern.ch/cms/data/CMSSW"

cat << CMS_EOF >> ./sources
RecoParticleFlow/PFBlockProducer/data/resmap_ECAL_eta.dat
RecoParticleFlow/PFBlockProducer/data/resmap_ECAL_phi.dat
RecoParticleFlow/PFBlockProducer/data/resmap_HCAL_eta.dat
RecoParticleFlow/PFBlockProducer/data/resmap_HCAL_phi.dat
CMS_EOF

## IMPORT data-package-build
