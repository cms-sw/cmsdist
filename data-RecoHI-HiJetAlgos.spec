### RPM cms data-RecoHI-HiJetAlgos V01-00-00

%prep

# Base URL, where to find the files
%define base_url "http://cmsdoc.cern.ch/cms/data/CMSSW"

cat << CMS_EOF >> ./sources
RecoHI/HiJetAlgos/data/ue_calibrations_calo_data.txt
RecoHI/HiJetAlgos/data/ue_calibrations_calo_mc.txt
RecoHI/HiJetAlgos/data/ue_calibrations_pf_data.txt
RecoHI/HiJetAlgos/data/ue_calibrations_pf_mc.txt
CMS_EOF

## IMPORT data-package-build
