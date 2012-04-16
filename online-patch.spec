### RPM cms online-patch CMSSW_5_2_4_onlpatch1_ONLINE
Requires: online-patch-tool-conf

%define useCmsTC        yes
%define saveDeps        yes
%define subpackageDebug yes

%define patchsrc2       perl -p -i -e ' s!(<classpath.*/test\\+.*>)!!' config/BuildFile.xml

#Set it to -cmsX added by cmsBuild (if any) to the base release
%define baserel_postfix %{nil}

## IMPORT cmssw-partial-build
## IMPORT cmssw-patch-build
## IMPORT scram-project-build
## SUBPACKAGE debug
