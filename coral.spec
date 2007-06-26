### RPM cms coral CORAL_1_7_2-cms147f
## IMPORT configurations
Provides: /bin/zsh
Requires: coral-tool-conf
Patch:    coral-SV1BuildFiles

%define toolconf        ${CORAL_TOOL_CONF_ROOT}/configurations/tools-STANDALONE.conf
%define cvsprojuc       %(echo %n | sed -e "s|-debug||"| tr 'a-z' 'A-Z')
%define cvsprojlc       %(echo %cvsprojuc | tr 'A-Z' 'a-z')
%define cvsdir          %cvsprojlc
%define cvsserver       %cvsprojlc
%define conflevel       %{nil}
%define prebuildtarget  prebuild
%define buildtarget     release-build
%define patchsrc        %patch -p0

## IMPORT lcg-scram-build
## IMPORT cms-scram-build
## IMPORT scramv1-build
