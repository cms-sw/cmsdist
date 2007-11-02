### RPM cms coral CORAL_1_9_1-CMS18
## IMPORT configurations
Provides: /bin/zsh
Requires: coral-tool-conf
Patch:    coral-SV1BuildFiles

%define cvsprojuc       %(echo %n | sed -e "s|-debug||"| tr 'a-z' 'A-Z')
%define cvsprojlc       %(echo %cvsprojuc | tr 'A-Z' 'a-z')
%define cvsdir          %cvsprojlc
%define cvsserver       %cvsprojlc
%define preBuildCommand (rm -rf LFCLookupService LFCReplicaService MySQLAccess)
%define prebuildtarget  prebuild
%define buildtarget     release-build
%define patchsrc        %patch -p0
%define patchsrc2       rm -rf %{srctree}/Tests/*

## IMPORT lcg-scram-build
## IMPORT cms-scram-build
## IMPORT scramv1-build
