### RPM cms data-CalibCalorimetry-CaloMiscalibTools V01-00-00

%prep

# Base URL, where to find the files
%define base_url "http://cmsdoc.cern.ch/cms/data/CMSSW"

cat << CMS_EOF >> ./sources
CalibCalorimetry/CaloMiscalibTools/data/EcalIntercalibConstants_EB_10pb.xml
CalibCalorimetry/CaloMiscalibTools/data/EcalIntercalibConstants_EB_ideal.xml
CalibCalorimetry/CaloMiscalibTools/data/EcalIntercalibConstants_EB_startup.xml
CalibCalorimetry/CaloMiscalibTools/data/EcalIntercalibConstants_EE_10pb.xml
CalibCalorimetry/CaloMiscalibTools/data/EcalIntercalibConstants_EE_ideal.xml
CalibCalorimetry/CaloMiscalibTools/data/EcalIntercalibConstants_EE_startup.xml
CalibCalorimetry/CaloMiscalibTools/data/hcalmiscalib_0.0.xml
CalibCalorimetry/CaloMiscalibTools/data/miscalib_barrel_10pb_csa08.xml
CalibCalorimetry/CaloMiscalibTools/data/miscalib_barrel_startup_csa08.xml
CalibCalorimetry/CaloMiscalibTools/data/miscalib_endcap_10pb_csa08.xml
CalibCalorimetry/CaloMiscalibTools/data/miscalib_endcap_startup_csa08.xml
CMS_EOF

## IMPORT data-package-build
