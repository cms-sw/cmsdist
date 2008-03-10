### RPM cms coral CORAL_1_9_2-CMS18l
## IMPORT configurations
Provides: /bin/zsh
Provides: libexpat.so.0
Requires: coral-tool-conf
Patch:    coral-1_9_1-SV1BuildFiles
Patch1:   coral-1_9_2-FrontierAccess

%define cvsprojuc       %(echo %n | sed -e "s|-debug||"| tr 'a-z' 'A-Z')
%define cvsprojlc       %(echo %cvsprojuc | tr 'A-Z' 'a-z')
%define cvsdir          %cvsprojlc
%define cvsserver       %cvsprojlc
%define preBuildCommand (rm -rf LFCLookupService LFCReplicaService MySQLAccess)
%define prebuildtarget  prebuild
%define buildtarget     release-build
%define patchsrc        %patch -p0
%define patchsrc2       %patch1 -p0
%define patchsrc3       rm -rf %{srctree}/Tests/*

%if "%{?online_release:set}" == "set"
# Disable building tests in online release,
# since they bring dependency on cppunit:
%define patchsrc4 	perl -p -i -e ' s!(<ClassPath.*/tests\\+.*>)!#$1!;' config/BuildFile
%endif

## IMPORT lcg-scram-build
## IMPORT cms-scram-build
## IMPORT scramv1-build
