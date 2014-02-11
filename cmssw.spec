### RPM cms cmssw CMSSW_4_4_6
Requires: cmssw-tool-conf python cms-git-tools

%define runGlimpse      yes
%define useCmsTC        yes
%define saveDeps        yes
%define branch          CMSSW_4_4_X
%define source1         git://github.com/cms-sw/cmssw.git?protocol=https&obj=%{branch}/%{realversion}&module=%{cvssrc}&export=%{srctree}&output=/src.tar.gz

## IMPORT scram-project-build
