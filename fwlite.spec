### RPM cms fwlite CMSSW_14_1_3_FWLITE

Requires: fwlite-tool-conf

%define saveDeps        yes
%define branch          CMSSW_7_0_X
%define gitcommit       %(echo %realversion | sed -e 's|_FWLITE||')

# Switch off building tests
%define patchsrc perl -p -i -e ' s|(<classpath.*test\\+test.*>)||;' config/BuildFile.xml*

#patch to build fwlite release; this should be fixed in cmssw
%define patchsrc2 rm -rf src/CommonTools/Utils/src/TMVAEvaluator.cc src/CommonTools/Utils/plugins/BuildFile.xml src/FWCore/Framework/bin

# depends on MessageService, which pulls in service dependencies
%define patchsrc3 rm -f src/FWCore/MessageLogger/python/MessageLogger_cfi.py

%define source1 git://github.com/cms-sw/cmssw.git?protocol=https&obj=%{branch}/%{gitcommit}&module=%{cvssrc}&export=%{srctree}&output=/src.tar.gz

## INCLUDE cmssw-partial-build
## INCLUDE scram-project-build
