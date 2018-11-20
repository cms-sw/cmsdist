### RPM cms data-Validation-Geometry V00-07-00

%prep

# Base URL, where to find the files
%define base_url "http://cmsdoc.cern.ch/cms/data/CMSSW"

cat << CMS_EOF >> ./sources
Validation/Geometry/data/single_neutrino.random.dat
CMS_EOF

## IMPORT data-package-build
