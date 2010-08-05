### RPM cms fwlite CMSSW_3_6_2_FWLITE

Requires: fwlite-tool-conf python

%define useCmsTC        yes
%define saveDeps        yes

# Skip library load and symbol checks to avoid dependency on seal:
#%define nolibchecks     on

# Switch off building tests
%define patchsrc perl -p -i -e ' s|(<classpath.*test\\+test.*>)||;' config/BuildFile.xml*
%define patchsrc2 rm -rf src/DataFormats/GeometrySurface/plugins

## IMPORT cmssw-partial-build
## IMPORT scram-project-build
