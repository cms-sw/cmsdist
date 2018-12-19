### RPM cms data-FastSimulation-MaterialEffects V05-00-00

%prep

# Base URL, where to find the files
%define base_url "http://cmsdoc.cern.ch/cms/data/CMSSW"

cat << CMS_EOF >> ./sources
FastSimulation/MaterialEffects/data/NuclearInteractions.root
CMS_EOF

## IMPORT data-package-build
