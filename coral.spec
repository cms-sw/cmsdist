### RPM cms coral CORAL_1_6_2
## IMPORT configurations
Requires: coral-tool-conf

%define confversion %cmsConfiguration
%define toolconf ${CORAL_TOOL_CONF_ROOT}/configurations/tools-STANDALONE.conf

%define cvsdir coral
%define cvsserver CORAL

%define conflevel   %{nil}
%define srctree coral
%define cvssrc coral
%define bootstrapfile %_builddir/config/CORAL_bootsrc
%define reqfile %_builddir/config/CORAL_requirements

%define buildtarget release-build 

# NR: define tag and repository for project's config:
%define configtag V00-00-98
%define cvsconfig config


# NR: the lcgaawrappertag tag is also used as a flag 
# for lcg-scram-build to choose the right toolbox:
%define lcgaawrappertag CORAL_1_6_2

## IMPORT lcg-scram-build
## IMPORT scramv1-build
