### RPM cms data-RecoJets-JetProducers V05-10-12

%prep

# Base URL, where to find the files
%define base_url "http://cmsdoc.cern.ch/cms/data/CMSSW"

cat << CMS_EOF >> ./sources
RecoJets/JetProducers/data/TMVAClassification_5x_BDT_chsFullPlusRMS.weights.xml.gz
RecoJets/JetProducers/data/TMVAClassificationCategory_JetID_53X_Dec2012.weights.xml.gz
RecoJets/JetProducers/data/TMVAClassificationCategory_JetID_MET_53X_Dec2012.weights.xml.gz
RecoJets/JetProducers/data/TMVAClassification_PUJetID_JPT_BDTG.weights_F.xml.gz
RecoJets/JetProducers/data/TMVAClassification_PUJetID_JPT_BDTG.weights.xml.gz
CMS_EOF

## IMPORT data-package-build
