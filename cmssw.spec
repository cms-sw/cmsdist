### RPM cms cmssw CMSSW_4_1_9
Requires: cmssw-tool-conf python

%define runGlimpse      yes
%define useCmsTC        yes
%define saveDeps        yes
%define branch          CMSSW_4_1_X
%define source1         git://github.com/cms-sw/cmssw.git?protocol=https&obj=%{branch}/%{realversion}&module=%{cvssrc}&export=%{srctree}&output=/src.tar.gz

## IMPORT scram-project-build
