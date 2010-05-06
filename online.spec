### RPM cms online CMSSW_3_6_0_ONLINE

Requires: online-tool-conf python
Patch0: online_src

%define useCmsTC        yes
%define saveDeps        yes

%define patchsrc2       perl -p -i -e ' s!(<classpath.*/test\\+.*>)!!' config/BuildFile.xml
%define patchsrc3       %patch -p0

## IMPORT cmssw-partial-build
## IMPORT scram-project-build
