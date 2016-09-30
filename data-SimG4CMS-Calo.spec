### RPM cms data-SimG4CMS-Calo V03-01-00

%prep

# Base URL, where to find the files
%define base_url "https://cmssdt.cern.ch/SDT/data/CMSSW"

cat << CMS_EOF >> ./sources
SimG4CMS/Calo/data/HFShowerLibrary_npmt_noatt_eta4_16en_v4.root
SimG4CMS/Calo/data/HFShowerLibrary_oldpmt_noatt_eta4_16en_v3.root
CMS_EOF

## IMPORT data-package-build
