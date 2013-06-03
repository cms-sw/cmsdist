### RPM cms cmssw-debug CMSSW_0_8_0_pre4
## IMPORT configurations
Requires: cmssw-tool-conf python
%define toolconf ${CMSSW_TOOL_CONF_ROOT}/configurations/tools-STANDALONE.conf
%define cvsdir CMSSW
%define cvsserver cmssw
%define patchsrc perl -p -i -e 's!<select name=(MyODBC|ignominy|rulechecker)>!!' config/requirements ;
%define patchsrc2 perl -p -i -e 's!slc3_ia32_gcc323>!slc3_ia32_gcc323old>!;s!slc3_ia32_gcc323_dbg!slc3_ia32_gcc323!' config/BuildFile
%define confversion %cmsConfiguration
%define conflevel   _2
%define preBuildCommand (rm -rf SimMuon/DTDigitizer/test)
%define buildtarget release-build
%define buildarch export SCRAM_ARCH=%cmsplatf_dbg
## IMPORT cms-scram-build
## IMPORT scramv1-build

