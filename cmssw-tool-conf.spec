### RPM cms cmssw-tool-conf 17.0
# with cmsBuild, change the above version only when a new
# tool is added

Provides: libboost_regex-gcc-mt.so 
Provides: libboost_signals-gcc-mt.so 
Provides: libboost_thread-gcc-mt.so

Requires: fakesystem
Requires: gcc-toolfile
Requires: gmake
Requires: pcre
Requires: zlib
Requires: bz2lib
Requires: uuid
Requires: python
Requires: expat
Requires: openssl
Requires: db4
Requires: gdbm
Requires: gccxml
Requires: boost
Requires: gsl
Requires: clhep
Requires: root
Requires: roofit
Requires: xrootd
Requires: qt
Requires: castor
Requires: libpng
Requires: libjpg
Requires: dcap
Requires: oracle
Requires: oracle-env
Requires: libungif
Requires: libtiff
Requires: cppunit
Requires: frontier_client
Requires: sqlite
Requires: graphviz
Requires: xerces-c
Requires: systemtools
Requires: coral
Requires: xdaq
Requires: geant4
Requires: hepmc
Requires: heppdt
Requires: elementtree
Requires: sigcpp
Requires: mimetic
Requires: rulechecker
Requires: soqt
Requires: coin
Requires: curl
Requires: simage
Requires: tkonlinesw
Requires: meschach
Requires: glimpse
Requires: valgrind
Requires: google-perftools
Requires: fastjet
Requires: ktjet
Requires: herwig
Requires: lhapdf
Requires: pythia6
Requires: pythia8
Requires: jimmy
Requires: hector
Requires: alpgen
Requires: tauola
Requires: toprex
Requires: charybdis
Requires: photos
Requires: cmsswdata
Requires: dpm
Requires: evtgenlhc
Requires: mcdb
Requires: dbs-client
Requires: herwigpp
Requires: thepeg
Requires: libhepml
Requires: sherpa
Requires: python-ldap
Requires: millepede
Requires: gdb
Requires: pyqt
Requires: igprof-toolfile

%define skipreqtools jcompiler lhapdfwrapfull lhapdffull

## IMPORT scramv1-tool-conf
