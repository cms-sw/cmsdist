### RPM cms online-patch CMSSW_3_11_1_onlpatch1_ONLINE
Requires: online-patch-tool-conf

%define useCmsTC        yes
%define saveDeps        yes
%define subpackageDebug yes

%define patchsrc2       perl -p -i -e ' s!(<classpath.*/test\\+.*>)!!' config/BuildFile.xml

#use of diff config tag in order to build patch release
#without rebuilding full release
#this should go away when the fix is integratedin to full release too
%define configtag       V03-37-09-01

#Set it to -cmsX added by cmsBuild (if any) to the base release
%define baserel_postfix %{nil}

## IMPORT cmssw-partial-build
## IMPORT cmssw-patch-build
## IMPORT scram-project-build
## SUBPACKAGE debug
