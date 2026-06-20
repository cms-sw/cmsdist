### RPM cms cmssw CMSSW_12_6_0_G41142

Requires: cmssw-tool-conf

%define runGlimpse      yes
%define saveDeps        yes
%define branch          CMSSW_12_6_X
%define gitcommit       16f30525e8dace04e24859879e9f75e201da1ebe
# build with debug symbols, and package them in a separate rpm
#define subpackageDebug yes

# Geant4 fixes #43004, #43048, #46675, #50950
Patch2: cmssw-geant4

## INCLUDE cmssw-queue-override

%define source1         git://github.com/cms-sw/cmssw.git?protocol=https&obj=%{branch}/%{gitcommit}&module=%{cvssrc}&export=%{srctree}&output=/src.tar.gz

%define patchsrc2 pushd src; patch -p1 <%{_sourcedir}/cmssw-geant4 ; popd

## IMPORT scram-project-build
## SUBPACKAGE debug IF %subpackageDebug
