### RPM cms fwlite CMSSW_3_8_7_FWLITE

Requires: fwlite-tool-conf python

%define useCmsTC        yes
%define saveDeps        yes

# Switch off building tests
%define patchsrc perl -p -i -e ' s|(<classpath.*test\\+test.*>)||;' config/BuildFile.xml*

# Includes parts of the framework that we don't want in fwlite
%define patchsrc2 rm -rf src/DataFormats/GeometrySurface/plugins

# depends on RecoEgamma/EgammaTools, which adds too many other dependencies; should be fixed in 39x
%define patchsrc3 rm -f src/PhysicsTools/SelectorUtils/src/SimpleCutBasedElectronIDSelectionFunctor.cc

## IMPORT cmssw-partial-build
## IMPORT scram-project-build
