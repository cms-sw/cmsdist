### RPM cms fwlite CMSSW_20_1_X_2026-09-01-2300_FWLITE

Requires: fwlite-tool-conf

%define saveDeps        yes
%define branch          CMSSW_7_0_X
%define gitcommit       %(echo %realversion | sed -e 's|_FWLITE||')

# depends on MessageService, which pulls in service dependencies
%define patchsrc2 rm -f src/FWCore/MessageLogger/python/MessageLogger_cfi.py

# delete various plugins and test directories
%define patchsrc3 rm -rf src/CommonTools/Utils/src/TMVAEvaluator.cc src/FWCore/Framework/bin src/*/*/test src/DataFormats/*/plugins src/Heterogeneous*/*/plugins src/CommonTools/Utils/plugins

%define source1 git://github.com/cms-sw/cmssw.git?protocol=https&obj=%{branch}/%{gitcommit}&module=%{cvssrc}&export=%{srctree}&output=/src.tar.gz

## INCLUDE cmssw-partial-build
## INCLUDE scram-project-build
