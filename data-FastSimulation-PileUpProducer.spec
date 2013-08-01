### RPM cms data-FastSimulation-PileUpProducer V04-05-18

%prep

# Base URL, where to find the files
%define base_url "http://cmsdoc.cern.ch/cms/data/CMSSW"

cat << CMS_EOF >> ./sources
FastSimulation/PileUpProducer/data/MinBias8TeV_001.root
FastSimulation/PileUpProducer/data/MinBias8TeV_002.root
FastSimulation/PileUpProducer/data/MinBias8TeV_003.root
FastSimulation/PileUpProducer/data/MinBias8TeV_004.root
FastSimulation/PileUpProducer/data/MinBias8TeV_005.root
FastSimulation/PileUpProducer/data/MinBias8TeV_006.root
FastSimulation/PileUpProducer/data/MinBias8TeV_007.root
FastSimulation/PileUpProducer/data/MinBias8TeV_008.root
FastSimulation/PileUpProducer/data/MinBias8TeV_009.root
FastSimulation/PileUpProducer/data/MinBias8TeV_010.root
FastSimulation/PileUpProducer/data/MinBias7TeV_001.root
FastSimulation/PileUpProducer/data/MinBias7TeV_002.root
FastSimulation/PileUpProducer/data/MinBias7TeV_003.root
FastSimulation/PileUpProducer/data/MinBias7TeV_004.root
FastSimulation/PileUpProducer/data/MinBias7TeV_005.root
FastSimulation/PileUpProducer/data/MinBias7TeV_006.root
FastSimulation/PileUpProducer/data/MinBias7TeV_007.root
FastSimulation/PileUpProducer/data/MinBias7TeV_008.root
FastSimulation/PileUpProducer/data/MinBias7TeV_009.root
FastSimulation/PileUpProducer/data/MinBias7TeV_010.root
FastSimulation/PileUpProducer/data/MinBias14TeV_001.root
FastSimulation/PileUpProducer/data/MinBias14TeV_002.root
FastSimulation/PileUpProducer/data/MinBias14TeV_003.root
FastSimulation/PileUpProducer/data/MinBias14TeV_004.root
FastSimulation/PileUpProducer/data/MinBias14TeV_005.root
FastSimulation/PileUpProducer/data/MinBias14TeV_006.root
FastSimulation/PileUpProducer/data/MinBias14TeV_007.root
FastSimulation/PileUpProducer/data/MinBias14TeV_008.root
FastSimulation/PileUpProducer/data/MinBias14TeV_009.root
FastSimulation/PileUpProducer/data/MinBias14TeV_010.root
CMS_EOF

## IMPORT data-package-build
