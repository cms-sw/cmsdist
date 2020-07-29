### RPM cms data-SimG4CMS-Forward V02-03-19

%prep

# Base URL, where to find the files
%define base_url "http://cmsdoc.cern.ch/cms/data/CMSSW"

cat << CMS_EOF >> ./sources
SimG4CMS/Forward/data/CastorShowerLibrary_CMSSW500_Standard.root
CMS_EOF

## IMPORT data-package-build
