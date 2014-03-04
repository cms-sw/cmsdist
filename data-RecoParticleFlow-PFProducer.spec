### RPM cms data-RecoParticleFlow-PFProducer V14-08-05

%prep

# Base URL, where to find the files
%define base_url "http://cmsdoc.cern.ch/cms/data/CMSSW"

cat << CMS_EOF >> ./sources
RecoParticleFlow/PFProducer/data/v2/MVAnalysis_BDT.weights_finalID_hzz-pions.txt
RecoParticleFlow/PFProducer/data/MVAnalysis_MLP.weights.txt
RecoParticleFlow/PFProducer/data/v2/MVAnalysis_BDT.weights_PfElectrons23Jan.txt
RecoParticleFlow/PFProducer/data/v2/MVAnalysis_BDT.weights_PfElectrons23Jan_IntToFloat.txt
RecoParticleFlow/PFProducer/data/v2/MVAnalysis_BDT.weights_pfConversionAug0411.txt
RecoParticleFlow/PFProducer/data/TMVARegression_BDTG_PFClusterCorr.root
RecoParticleFlow/PFProducer/data/TMVARegression_BDTG_PFGlobalCorr.root
RecoParticleFlow/PFProducer/data/allX0histos.root
RecoParticleFlow/PFProducer/data/TMVARegression_BDTG_PFRes.root
CMS_EOF

## IMPORT data-package-build
