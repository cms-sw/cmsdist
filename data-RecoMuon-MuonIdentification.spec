### RPM cms data-RecoMuon-MuonIdentification V01-12-01

%prep

# Base URL, where to find the files
%define base_url "http://cmsdoc.cern.ch/cms/data/CMSSW"

cat << CMS_EOF >> ./sources
RecoMuon/MuonIdentification/data/MuID_templates_pions_lowPt_3_1_norm.root
RecoMuon/MuonIdentification/data/MuID_templates_muons_lowPt_3_1_norm.root
CMS_EOF

## IMPORT data-package-build
