### RPM cms coral CORAL_2_1_0
## IMPORT configurations 
Provides: /bin/zsh
Provides: libexpat.so.0
Requires: coral-tool-conf
Patch:    coral-2_1_0-SV1BuildFiles
Patch2:   coral-2_1_0-boost1.37.0

%define cvsprojuc       %(echo %n | sed -e "s|-debug||"| tr 'a-z' 'A-Z')
%define cvsprojlc       %(echo %cvsprojuc | tr 'A-Z' 'a-z')
%define cvsdir          %cvsprojlc
%define cvsserver       %cvsprojlc
%define preBuildCommand (rm -rf LFCLookupService LFCReplicaService MySQLAccess)
%define prebuildtarget  prebuild
%define buildtarget     release-build
%define patchsrc        %patch -p0
%define patchsrc2       %patch2 -p0
%define patchsrc3       rm -rf %{srctree}/Tests/*

%if "%cmsplatf" == "slc4onl_ia32_gcc346"
# Disable building tests in online release,
# since they bring dependency on cppunit:
%define patchsrc4       perl -p -i -e 's!(<classpath.*/tests\\+.*>)!!;' config/BuildFile.xml
%endif

## IMPORT lcg-scram-build
## IMPORT cms-scram-build
## IMPORT scramv1-build
