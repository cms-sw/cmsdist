### RPM cms online CMSSW_3_8_0_ONLINE

Requires: online-tool-conf python
Patch: online_src

%define useCmsTC        yes
%define saveDeps        yes

%define patchsrc        %patch -p0
%define patchsrc2       perl -p -i -e ' s!(<classpath.*/test\\+.*>)!!' config/BuildFile.xml

## IMPORT cmssw-partial-build
## IMPORT scram-project-build
