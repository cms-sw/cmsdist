### RPM cms cmssw-patch CMSSW_11_1_0_patch3
Requires: cmssw-patch-tool-conf 

%define runGlimpse      yes
%define saveDeps        yes
# build with debug symbols, and package them in a separate rpm
#subpackage debug disabledes

#Set it to -cmsX added by cmsBuild (if any) to the base release
%define baserel_postfix %{nil}

## INCLUDE cmssw-queue-override

## IMPORT cmssw-patch-build
## IMPORT scram-project-build
## SUBPACKAGE debug IF %subpackageDebug
