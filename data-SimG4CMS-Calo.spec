### RPM cms data-SimG4CMS-Calo V03-00-00

%prep

# Base URL, where to find the files
%define base_url "http://cmsdoc.cern.ch/cms/data/CMSSW"

cat << CMS_EOF >> ./sources
SimG4CMS/Calo/data/HFShowerLibrary_npmt_noatt_eta4_16en_v3.root
SimG4CMS/Calo/data/HFShowerLibrary_oldpmt_noatt_eta4_16en_v3.root
CMS_EOF

## IMPORT data-package-build
