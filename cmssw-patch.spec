### RPM cms cmssw-patch CMSSW_3_11_1_patch1
Requires: cmssw-patch-tool-conf 

%define runGlimpse      yes
%define saveDeps        yes
# build with debug symbols, and package them in a separate rpm
%define subpackageDebug yes

#Set it to -cmsX added by cmsBuild (if any) to the base release
%define baserel_postfix %{nil}

## INCLUDE cmssw-queue-override

## IMPORT cmssw-patch-build
## IMPORT scram-project-build
## SUBPACKAGE debug IF %subpackageDebug
# bla bla
