### RPM cms cmssw CMSSW_0_7_0_pre1
Requires: cmssw-tool-conf python
%define toolconf ${CMSSW_TOOL_CONF_ROOT}/configurations/tools-STANDALONE.conf
%define cvsdir %(echo %n | tr 'a-z' 'A-Z')
%define cvsserver %(echo %n | tr 'A-Z' 'a-z')
%define patchsrc perl -p -i -e 's!<select name=(MyODBC|ignominy|rulechecker|fed9uutils)>!!' config/requirements ;

%define confversion 134a
%define conflevel   _2
%define preBuildCommand (rm -rf SimMuon/DTDigitizer/test)
%define buildtarget release-build 
## IMPORT cms-scram-build
## IMPORT scramv1-build

