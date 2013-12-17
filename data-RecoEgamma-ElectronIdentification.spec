### RPM cms data-RecoEgamma-ElectronIdentification V00-03-35

%prep

# Base URL, where to find the files
%define base_url "http://cmsdoc.cern.ch/cms/data/CMSSW"

cat << CMS_EOF >> ./sources
RecoEgamma/ElectronIdentification/data/TMVA_BDTSimpleCat_17Feb2011.weights.xml
RecoEgamma/ElectronIdentification/data/TMVA_BDTSoftElectrons_9Dec2013.weights.xml
CMS_EOF

## IMPORT data-package-build
