### RPM cms cmssw-tool-conf CMS_152h

Provides: tmp/slc3_ia32_gcc323/src/FWCore/TFWLiteSelector/test/libFWCoreTFWLiteSelectorTest.so
Provides: libboost_regex-gcc-mt.so 
Provides: libboost_signals-gcc-mt.so 
Provides: libboost_thread-gcc-mt.so

Requires: pool
Requires: coral
Requires: seal
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
Requires: xrootd
Requires: qt
Requires: castor
Requires: mysql
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
Requires: xerces-c
Requires: p5-dbd-oracle
Requires: mysqlpp
Requires: systemtools
Requires: seal
Requires: coral
Requires: pool

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
Requires: doxygen
Requires: meschach
Requires: glimpse
Requires: valgrind
Requires: fastjet
Requires: ktjet
# Remove this dependency altogether for the moment, until the java issues
# are dealt with and igprof/ighook are migrated into CMSSW
## Remove this dependency (temporarily) for gcc4.x, 64bit and other builds,
## i.e. keep it only for the standard slc4_ia32_gcc345 build
#%if ("%cmsplatf" == "slc4_ia32_gcc345")
#Requires: ignominy
#%endif
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

%define skipreqtools jcompiler

## IMPORT scramv1-tool-conf
