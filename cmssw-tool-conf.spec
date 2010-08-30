### RPM cms cmssw-tool-conf 18.0
## NOCOMPILER
# with cmsBuild, change the above version only when a new
# tool is added

Provides: libboost_regex-gcc-mt.so 
Provides: libboost_signals-gcc-mt.so 
Provides: libboost_thread-gcc-mt.so

Requires: fakesystem
Requires: coral-toolfile
Requires: gcc-toolfile
Requires: gmake-toolfile
Requires: pcre-toolfile
Requires: zlib-toolfile
Requires: bz2lib-toolfile
Requires: uuid-toolfile
Requires: python-toolfile
Requires: expat-toolfile
Requires: openssl-toolfile
Requires: db4-toolfile
Requires: gdbm-toolfile
Requires: gccxml-toolfile
Requires: boost-toolfile
Requires: gsl-toolfile
Requires: clhep-toolfile
Requires: root-toolfile
Requires: roofit-toolfile
Requires: xrootd-toolfile
Requires: qt-toolfile
Requires: castor-toolfile
Requires: libpng-toolfile
Requires: libjpg-toolfile
Requires: dcap-toolfile
Requires: oracle-toolfile
Requires: oracle-env
Requires: libungif-toolfile
Requires: libtiff-toolfile
Requires: cppunit-toolfile
Requires: frontier_client-toolfile
Requires: sqlite-toolfile
Requires: graphviz-toolfile
Requires: xerces-c-toolfile
Requires: systemtools
Requires: xdaq-toolfile
Requires: geant4-toolfile
Requires: hepmc-toolfile
Requires: heppdt-toolfile
Requires: elementtree-toolfile
Requires: sigcpp-toolfile
Requires: mimetic-toolfile
Requires: rulechecker-toolfile
Requires: soqt-toolfile
Requires: coin-toolfile
Requires: curl-toolfile
Requires: simage-toolfile
Requires: tkonlinesw-toolfile
Requires: meschach-toolfile
Requires: glimpse-toolfile
Requires: valgrind-toolfile
Requires: google-perftools-toolfile
Requires: fastjet-toolfile
Requires: ktjet-toolfile
Requires: herwig-toolfile
Requires: lhapdf-toolfile
Requires: pythia6-toolfile
Requires: pythia8-toolfile
Requires: jimmy-toolfile
Requires: hector-toolfile
Requires: alpgen-toolfile
Requires: tauola-toolfile
Requires: toprex-toolfile
Requires: charybdis-toolfile
Requires: photos-toolfile
Requires: cmsswdata-toolfile
Requires: dpm-toolfile
Requires: evtgenlhc-toolfile
Requires: mcdb-toolfile
Requires: dbs-client-toolfile
Requires: herwigpp-toolfile
Requires: thepeg-toolfile
Requires: libhepml-toolfile
Requires: sherpa-toolfile
Requires: python-ldap-toolfile
Requires: openldap-toolfile
Requires: millepede-toolfile
Requires: gdb-toolfile
Requires: pyqt-toolfile
Requires: sip-toolfile
Requires: igprof-toolfile

%define skipreqtools jcompiler lhapdfwrapfull lhapdffull

## IMPORT scramv1-tool-conf
