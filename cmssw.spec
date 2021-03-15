### RPM cms cmssw CMSSW_11_3_X_2021-03-10-1200

Requires: cmssw-tool-conf python

%define runGlimpse      yes
%define saveDeps        yes
%define branch          master
%define gitcommit       CMSSW_11_3_X_2021-03-10-1100
# build with debug symbols, and package them in a separate rpm
#define subpackageDebug yes

## INCLUDE cmssw-queue-override

%define source1         git://github.com/cms-sw/cmssw.git?protocol=https&obj=%{branch}/%{gitcommit}&module=%{cvssrc}&export=%{srctree}&output=/src.tar.gz

## IMPORT scram-project-build
## SUBPACKAGE debug IF %subpackageDebug
