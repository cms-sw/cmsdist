### RPM cms coral CORAL_1_6_3a-p1
## IMPORT configurations
Provides: /bin/zsh
Requires: coral-tool-conf


# ATTENTION: wrappertag is only needed when tag in LCGAAwrappers differs
# from the release name. For normal releases it should be removed.
%define wrapperstag    CORAL_1_6_3a_nldlp
%define configtag nr070210_144a_noldlp

%define toolconf       ${CORAL_TOOL_CONF_ROOT}/configurations/tools-STANDALONE.conf
%define cvsprojuc      %(echo %n | sed -e "s|-debug||"| tr 'a-z' 'A-Z')
%define cvsprojlc      %(echo %cvsprojuc | tr 'A-Z' 'a-z')
%define cvsdir         %cvsprojlc
%define cvsserver      %cvsprojlc
%define cvsconfig      config
%define confversion    %cmsConfiguration
%define conflevel      %{nil}
%define prebuildtarget prebuild
%define buildtarget    release-build
%define bootstrapfile  %_builddir/%{cvsconfig}/%{cvsprojuc}_bootsrc
%define reqfile        %_builddir/%{cvsconfig}/%{cvsprojuc}_requirements

## IMPORT lcg-scram-build
## IMPORT scramv1-build
