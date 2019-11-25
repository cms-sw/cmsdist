### RPM cms fwlite CMSSW_7_1_45_FWLITE

Requires: fwlite-tool-conf python

%define useCmsTC        yes
%define saveDeps        yes

# Switch off building tests
%define patchsrc perl -p -i -e ' s|(<classpath.*test\\+test.*>)||;' config/BuildFile.xml*

# Includes parts of the framework that we don't want in fwlite
%define patchsrc2 rm -rf src/DataFormats/GeometrySurface/plugins

# depends on MessageService, which pulls in service dependencies
%define patchsrc3 rm -f src/FWCore/MessageLogger/python/MessageLogger_cfi.py

## IMPORT cmssw-partial-build
## IMPORT scram-project-build
