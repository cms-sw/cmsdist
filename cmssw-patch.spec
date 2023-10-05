### RPM cms cmssw-patch CMSSW_13_2_5_patch3
Requires: cmssw-patch-tool-conf 

%define runGlimpse      yes
%define saveDeps        yes
# build with debug symbols, and package them in a separate rpm
#subpackage debug disabledes

#Set it to -cmsX added by cmsBuild (if any) to the base release
%define baserel_postfix %{nil}

## SUBPACKAGE debug IF %subpackageDebug
## INCLUDE cmssw-queue-override
## INCLUDE cmssw-patch-build
## INCLUDE scram-project-build
