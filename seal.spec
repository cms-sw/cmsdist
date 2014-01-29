### RPM cms seal SEAL_1_9_4
## IMPORT configurations
Provides: /bin/zsh
Requires: seal-tool-conf
Patch:    seal-SV1BuildFiles

%define cvsprojuc       %(echo %n | sed -e "s|-debug||"| tr 'a-z' 'A-Z')
%define cvsprojlc       %(echo %cvsprojuc | tr 'A-Z' 'a-z')
%define cvsdir          %cvsprojuc
%define cvsserver       %cvsprojlc
%define preBuildCommand (rm -rf Extensions MathLibs Documentation config)
%define prebuildtarget  prebuild
%define buildtarget     release-build
%define patchsrc        %patch -p0

%if "%{?online_release:set}" == "set"
# Disable building tests in online release, 
# since they bring dependency on cppunit:
%define patchsrc2     perl -p -i -e ' s!(<classpath.*/tests\\+.*>)!!;' config/BuildFile.xml
%endif

%if "%cmsplatf" == "osx105_ia32_gcc401"
# Disable building tests for mac as well, 
# since they bring dependency on cppunit:
%define patchsrc2     perl -p -i -e ' s!(<classpath.*/tests\\+.*>)!!;' config/BuildFile.xml
%endif


## IMPORT lcg-scram-build
## IMPORT cms-scram-build
## IMPORT scramv1-build
