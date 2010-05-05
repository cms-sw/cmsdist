### RPM cms online-patch CMSSW_3_5_7_onlpatch2_ONLINE

Requires: online-patch-tool-conf

%define useCmsTC        yes
%define saveDeps        yes

%define patchsrc2       perl -p -i -e ' s!(<classpath.*/test\\+.*>)!!' config/BuildFile.xml

#Set it to -cmsX added by cmsBuild (if any due to a rebuild) to the base release
%define baserel_postfix %{nil}

## IMPORT cmssw-partial-build
## IMPORT cmssw-patch-build
## IMPORT scram-project-build
