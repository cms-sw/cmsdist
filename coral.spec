### RPM lcg coral CORAL_1_2_0
Requires: coral-tool-conf
%define confversion 40 
%define toolconf ${CORAL_TOOL_CONF_ROOT}/configurations/tools-STANDALONE.conf
%define cvsdir %(echo %n | tr 'A-Z' 'a-z')
%define cvsserver %(echo %n | tr 'A-Z' 'a-z')
# This allows to compile CORAL on linux systems that are not recognized as slc3 but still linux based.
%define patchsrc if [ "%cmsplatf" != "slc3_ia32_gcc323" ] && [ "$(uname)" = "Linux" ]; then cp config/slc3_ia32_gcc323.mk config/%{cmsplatf}.mk; fi 
## IMPORT lcg-scram-build
## IMPORT scram-build

%define conflevel   _1	
# FIXME: Remove when it successfully builds... should just be release
%define buildtarget	release-build release-docs release-freeze
#%define buildtarget %{nil}
