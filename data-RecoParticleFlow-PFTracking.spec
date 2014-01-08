### RPM cms data-RecoParticleFlow-PFTracking V12-03-03

%prep

# Base URL, where to find the files
%define base_url "http://cmsdoc.cern.ch/cms/data/CMSSW"

cat << CMS_EOF >> ./sources
RecoParticleFlow/PFTracking/data/BDT_weights_21.txt
RecoParticleFlow/PFTracking/data/MVAnalysis_BDT.weights_convBremFinder_19Apr.txt
RecoParticleFlow/PFTracking/data/MVAnalysis_BDT.weights_convBremFinder_19Apr_IntToFloat.txt
RecoParticleFlow/PFTracking/data/TMVAClassification_ConvBremFinder_Testetgt20absetagt1_479_BDT.weights.xml
RecoParticleFlow/PFTracking/data/TMVAClassification_ConvBremFinder_Testetgt20absetalt1_479_BDT.weights.xml
RecoParticleFlow/PFTracking/data/TMVAClassification_ConvBremFinder_Testetlt20absetagt1_479_BDT.weights.xml
RecoParticleFlow/PFTracking/data/TMVAClassification_ConvBremFinder_Testetlt20absetalt1_479_BDT.weights.xml
CMS_EOF

## IMPORT data-package-build
