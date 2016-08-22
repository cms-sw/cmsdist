### RPM cms fwlite CMSSW_8_1_0_pre9_FWLITE

Requires: fwlite-tool-conf python

%define saveDeps        yes
%define branch          CMSSW_7_0_X
%define gitcommit       %(echo %realversion | sed -e 's|_FWLITE||')

# Switch off building tests
%define patchsrc perl -p -i -e ' s|(<classpath.*test\\+test.*>)||;' config/BuildFile.xml*

#patch to build fwlite release; this should be fixed in cmssw
%define patchsrc2 rm -f src/CommonTools/Utils/src/TMVAEvaluator.cc src/CommonTools/Utils/plugins/BuildFile.xml

# depends on MessageService, which pulls in service dependencies
%define patchsrc3 rm -f src/FWCore/MessageLogger/python/MessageLogger_cfi.py


# depends on CondFormats/EgammaObjects/interface/GBRForest.h which pulls in to many dependencies for fwlite
%define patchsrc4 rm -f src/CommonTools/Utils/src/TMVAEvaluator.cc
%define patchsrc5 rm -rf src/CommonTools/Utils/plugins

%define patchsrc6 rm -rf  src/CondFormats/RPCObjects/test/* src/CondFormats/RPCObjects/src/*
%define patchsrc7 rm -rf  src/CondFormats/L1TObjects/test/* src/CondFormats/L1TObjects/src/*
%define patchsrc8 perl -p -i -e 's|<use   name="DataFormats/Candidate"/>|<use   name="DataFormats/Candidate"/> <use   name="DataFormats/HcalRecHit"/>|' src/DataFormats/CastorReco/BuildFile.xml
%define patchsrc12 find src -name BuildFile.xml | xargs grep rootcore | cut -d: -f1 | uniq | grep -v "DataFormats/StdDictionaries" | xargs perl -p -i -e's|name="rootcore"/>|name="rootcore"/> <use name="DataFormats/StdDictionaries"/>|'  
%define patchsrc13 find src -name BuildFile.xml | xargs grep rootinteractive | cut -d: -f1 | uniq | grep -v "DataFormats/StdDictionaries" | xargs perl -p -i -e's|name="rootinteractive"/>|name="rootinteractive"/> <use name="DataFormats/StdDictionaries"/>|'  
%define patchsrc14 perl -p -i -e 's|<use   name="CondFormats/RPCObjects"/>||' src/DataFormats/RPCDigi/BuildFile.xml
%define patchsrc15 perl -p -i -e 's|<use   name="CondFormats/L1TObjects"/>||' src/DataFormats/PatCandidates/BuildFile.xml
%define patchsrc16 perl -p -i -e 's|<use   name="DataFormats/TrackReco"/>|<use   name="DataFormats/TrackReco"/> <use   name="DataFormats/MuonReco"/>|' src/DataFormats/ParticleFlowReco/BuildFile.xml
%define patchsrc17 perl -p -i -e 's|<use   name="SimDataFormats/GeneratorProducts"/>|<use   name="SimDataFormats/GeneratorProducts"/>  <use   name="SimDataFormats/TrackingAnalysis"/>|' src/DataFormats/RecoCandidate/BuildFile.xml


%define source1 git://github.com/cms-sw/cmssw.git?protocol=https&obj=%{branch}/%{gitcommit}&module=%{cvssrc}&export=%{srctree}&output=/src.tar.gz

## IMPORT cmssw-partial-build
## IMPORT scram-project-build
