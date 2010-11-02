### RPM cms fwlite CMSSW_3_6_1_FWLITE

Requires: fwlite-tool-conf python

%define useCmsTC        yes
%define saveDeps        yes

# Skip library load and symbol checks to avoid dependency on seal:
%define nolibchecks     on

# Switch off building tests
%define patchsrc3 perl -p -i -e ' s|(<classpath.*test\\+test.*>)||;' config/BuildFile.xml*

## IMPORT cmssw-partial-build
## IMPORT scram-project-build
