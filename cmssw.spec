### RPM cms cmssw CMSSW_12_6_0_G41141

Requires: cmssw-tool-conf

%define runGlimpse      yes
%define saveDeps        yes
%define branch          CMSSW_12_6_X
%define gitcommit       16f30525e8dace04e24859879e9f75e201da1ebe
# build with debug symbols, and package them in a separate rpm
#define subpackageDebug yes
Patch2: cmssw-43004
Patch3: cmssw-43048
Patch4: cmssw-46675

## INCLUDE cmssw-queue-override

%define source1         git://github.com/cms-sw/cmssw.git?protocol=https&obj=%{branch}/%{gitcommit}&module=%{cvssrc}&export=%{srctree}&output=/src.tar.gz
%define patchsrc2 %patch2 -p1
%define patchsrc3 %patch3 -p1
%define patchsrc4 %patch4 -p1


## IMPORT scram-project-build
## SUBPACKAGE debug IF %subpackageDebug
