### RPM cms online CMSSW_3_6_3_ONLINE

Requires: online-tool-conf python

%define useCmsTC        yes
%define saveDeps        yes

%define patchsrc2       perl -p -i -e ' s!(<classpath.*/test\\+.*>)!!' config/BuildFile.xml

## IMPORT cmssw-partial-build
## IMPORT scram-project-build
