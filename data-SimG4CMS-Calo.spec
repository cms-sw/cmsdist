### RPM cms data-SimG4CMS-Calo V02-03-07

%prep

# Base URL, where to find the files
%define base_url "http://cmsdoc.cern.ch/cms/data/CMSSW"

cat << CMS_EOF >> ./sources
SimG4CMS/Calo/data/hfshowerlibrary_lhep_140_edm.root
SimG4CMS/Calo/data/HFShowerLibrary_npmt_eta4_16en.root
CMS_EOF

## IMPORT data-package-build
