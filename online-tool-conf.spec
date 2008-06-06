### RPM cms online-tool-conf 4.0
# with cmsBuild, change the above version only when a new
# tool is added
## INITENV SET CMSSW_TOOL_CONF_ROOT $ONLINE_TOOL_CONF_ROOT
Provides: tmp/slc3_ia32_gcc323/src/FWCore/TFWLiteSelector/test/libFWCoreTFWLiteSelectorTest.so
Provides: libboost_regex-gcc-mt.so 
Provides: libboost_signals-gcc-mt.so 
Provides: libboost_thread-gcc-mt.so

Requires: pool
Requires: coral
Requires: seal
Requires: gmake
Requires: pcre
Requires: bz2lib
Requires: uuid
Requires: python
Requires: expat
Requires: gccxml
Requires: boost
Requires: gsl
Requires: clhep
Requires: root
Requires: qt
Requires: castor
Requires: libjpg
Requires: libtiff
Requires: dcap
Requires: p5-dbd-oracle
Requires: frontier_client
Requires: sqlite
Requires: hepmc
Requires: heppdt
Requires: elementtree
Requires: sigcpp
Requires: tkonlinesw
Requires: fastjet
Requires: ktjet
Requires: dpm
Requires: oracle-env
Requires: onlinesystemtools


%define skipreqtools jcompiler
%define onlinesystemtoolsroot ${ONLINESYSTEMTOOLS_ROOT}
## IMPORT scramv1-tool-conf
