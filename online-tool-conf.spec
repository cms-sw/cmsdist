### RPM cms online-tool-conf CMS_150onl

Provides: tmp/slc3_ia32_gcc323/src/FWCore/TFWLiteSelector/test/libFWCoreTFWLiteSelectorTest.so
Provides: libboost_regex-gcc-mt.so 
Provides: libboost_signals-gcc-mt.so 
Provides: libboost_thread-gcc-mt.so

Requires: pool
Requires: coral
Requires: seal
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
Requires: dcap
Requires: oracle-env
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
Requires: onlinesystemtools


%define skipreqtools jcompiler
%define onlinesystemtoolsroot ${ONLINESYSTEMTOOLS_ROOT}
## IMPORT scramv1-tool-conf
