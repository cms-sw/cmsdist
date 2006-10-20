### RPM lcg coral CORAL_1_5_3-for106
## IMPORT configurations
Requires: coral-tool-conf
Patch: CORAL_1_5_3-crashandperformance
%define confversion %lcgConfiguration 
%define toolconf ${CORAL_TOOL_CONF_ROOT}/configurations/tools-STANDALONE.conf
%define cvsdir coral
%define cvsserver CORAL
%define srctree coral
%define configtree coral/config/scram
# This allows to compile CORAL on linux systems that are not recognized as slc3 but still linux based.
%define patchsrc if [ "%cmsplatf" != "slc3_ia32_gcc323" ] && [ "$(uname)" = "Linux" ]; then cp %{configtree}/slc3_ia32_gcc323.mk %{configtree}/%{cmsplatf}.mk; fi 
%define patchsrc2 perl -p -i -e "s|(project name=CORAL version=).*>|project name=CORAL version=%v>/BootStrapFileSRC|" %{configtree}/BootStrapFileSRC
%define patchsrc3 rm -rf %{srctree}/SQLiteAccess/tests
%define patchsrc4 %%patch0
%define patchinstall mkdir -p %{i}/include; for x in `ls %{i}/src`; do if [ -d %{i}/src/$x/$x ]; then cp -r %{i}/src/$x/$x %{i}/include; fi ; done

%define conflevel   _1
# FIXME: Remove when it successfully builds... should just be release
%define buildtarget release-build release-docs release-freeze
#%define buildtarget %{nil}

## IMPORT lcg-scram-build
## IMPORT scram-build
#
