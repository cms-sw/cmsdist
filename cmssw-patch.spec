### RPM cms cmssw-patch CMSSW_3_11_1_patch1
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
