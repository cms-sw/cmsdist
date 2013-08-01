### RPM cms data-RecoParticleFlow-PFTracking V12-03-02

%prep

# Base URL, where to find the files
%define base_url "http://cmsdoc.cern.ch/cms/data/CMSSW"

cat << CMS_EOF >> ./sources
RecoParticleFlow/PFTracking/data/BDT_weights_21.txt
RecoParticleFlow/PFTracking/data/MVAnalysis_BDT.weights_convBremFinder_19Apr.txt
RecoParticleFlow/PFTracking/data/MVAnalysis_BDT.weights_convBremFinder_19Apr_IntToFloat.txt
CMS_EOF

## IMPORT data-package-build
