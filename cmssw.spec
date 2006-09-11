### RPM cms cmssw CMSSW_1_0_0_pre5
## IMPORT configurations

Provides: /bin/zsh
Requires: cmssw-tool-conf python
%define toolconf ${CMSSW_TOOL_CONF_ROOT}/configurations/tools-STANDALONE.conf
%define cvsdir %(echo %n | tr 'a-z' 'A-Z')
%define cvsserver %(echo %n | tr 'A-Z' 'a-z')
%define patchsrc perl -p -i -e 's!<select name=(MyODBC|ignominy|rulechecker)>!!' config/requirements ;
%define confversion %cmsConfiguration
%define conflevel   _2
%define buildtarget release-build doc 
## IMPORT cms-scram-build
## IMPORT scramv1-build

