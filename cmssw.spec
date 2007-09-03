### RPM cms cmssw CMSSW_1_6_0
## IMPORT configurations 
Provides: /bin/zsh
Requires: cmssw-tool-conf python glimpse

%define toolconf        ${CMSSW_TOOL_CONF_ROOT}/configurations/tools-STANDALONE.conf
%define cvsprojuc       %(echo %n | sed -e "s|-debug||"| tr 'a-z' 'A-Z')
%define cvsprojlc       %(echo %cvsprojuc | tr 'A-Z' 'a-z')
%define cvsdir          %cvsprojuc
%define cvsserver       %cvsprojlc
%define conflevel       _2
%define prebuildtarget  gindices
%define buildtarget     release-build
%define patchsrc perl -p -i -e 's!<select name=(MyODBC)>!!' config/requirements ;
%define useCmsTC        1

## IMPORT cms-scram-build
## IMPORT scramv1-build
