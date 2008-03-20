### RPM cms fwlite-tool-conf CMS_151l
## INITENV SET CMSSW_TOOL_CONF_ROOT $FWLITE_TOOL_CONF_ROOT
Provides: tmp/slc3_ia32_gcc323/src/FWCore/TFWLiteSelector/test/libFWCoreTFWLiteSelectorTest.so
Provides: libboost_regex-gcc-mt.so 
Provides: libboost_signals-gcc-mt.so 
Provides: libboost_thread-gcc-mt.so

Requires: gcc
Requires: pcre
Requires: zlib
Requires: bz2lib
Requires: uuid
Requires: python
Requires: gccxml
Requires: boost
Requires: gsl
Requires: clhep
Requires: root
Requires: systemtools
Requires: hepmc
Requires: elementtree
Requires: sigcpp

%define skipreqtools jcompiler

## IMPORT scramv1-tool-conf
