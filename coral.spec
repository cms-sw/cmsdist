### RPM cms coral CORAL_LCG_54_pre2-CMS19f
## IMPORT configurations
Provides: /bin/zsh
Requires: coral-tool-conf
Patch:    coral-1_9_1-SV1BuildFiles
Patch1:   coral-1_9_2-FrontierAccess

%define cvsprojuc       %(echo %n | sed -e "s|-debug||"| tr 'a-z' 'A-Z')
%define cvsprojlc       %(echo %cvsprojuc | tr 'A-Z' 'a-z')
%define cvsdir          %cvsprojlc
%define cvsserver       %cvsprojlc
%define cvstag          LCG_54_pre2
%define preBuildCommand (rm -rf LFCLookupService LFCReplicaService MySQLAccess)
%define prebuildtarget  prebuild
%define buildtarget     release-build
%define patchsrc        %patch -p0
%define patchsrc2       %patch1 -p0
%define patchsrc3       rm -rf %{srctree}/Tests/*

## IMPORT lcg-scram-build
## IMPORT cms-scram-build
## IMPORT scramv1-build
