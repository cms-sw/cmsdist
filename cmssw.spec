### RPM cms cmssw CMSSW_0_6_0_pre1
Requires: cmssw-tool-conf
%define toolconf ${IGUANA_TOOL_CONF_ROOT}/configurations/tools-STANDALONE.conf
%define cvsdir %(echo %n | tr 'a-z' 'A-Z')
%define cvsserver %(echo %n | tr 'A-Z' 'a-z')

## IMPORT cms-scram-build
## IMPORT scramv1-build

%define confversion 132
%define conflevel   _2
