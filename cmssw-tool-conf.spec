### RPM cms cmssw-tool-conf 18.0
## NOCOMPILER
# with cmsBuild, change the above version only when a new
# tool is added

Provides: libboost_regex-gcc-mt.so 
Provides: libboost_signals-gcc-mt.so 
Provides: libboost_thread-gcc-mt.so
%define closingbrace )
%define isslc %(case %cmsos in slc*%closingbrace echo true;; *%closingbrace echo false;; esac)
%define is64bit %(case %cmsos in slc*_amd64%closingbrace echo true;; *%closingbrace echo false;; esac)

Requires: alpgen-toolfile
Requires: boost-toolfile
Requires: bz2lib-toolfile
Requires: castor-toolfile
Requires: charybdis-toolfile
Requires: clhep-toolfile
Requires: coin-toolfile
Requires: coral-toolfile
Requires: cppunit-toolfile
Requires: curl-toolfile
Requires: db4-toolfile
Requires: dbs-client-toolfile
Requires: dpm-toolfile
Requires: elementtree-toolfile
Requires: evtgenlhc-toolfile
Requires: expat-toolfile
Requires: fakesystem
Requires: fastjet-toolfile
Requires: gcc-toolfile
Requires: gccxml-toolfile
Requires: gdbm-toolfile
Requires: geant4-toolfile
Requires: glimpse-toolfile
Requires: gmake-toolfile
Requires: gsl-toolfile
Requires: hector-toolfile
Requires: hepmc-toolfile
Requires: heppdt-toolfile
Requires: herwig-toolfile
Requires: herwigpp-toolfile
Requires: jimmy-toolfile
Requires: ktjet-toolfile
Requires: lhapdf-toolfile
Requires: libhepml-toolfile
Requires: libjpg-toolfile
Requires: libpng-toolfile
Requires: libtiff-toolfile
Requires: libungif-toolfile
Requires: mcdb-toolfile
Requires: meschach-toolfile
Requires: millepede-toolfile
Requires: mimetic-toolfile
Requires: openldap-toolfile
Requires: openssl-toolfile
Requires: oracle-env
Requires: oracle-toolfile
Requires: pcre-toolfile
Requires: photos-toolfile
Requires: pool-toolfile
Requires: pythia6-toolfile
Requires: pythia8-toolfile
Requires: python-ldap-toolfile
Requires: python-toolfile
Requires: qt-toolfile
Requires: roofit-toolfile
Requires: root-toolfile
Requires: sherpa-toolfile
Requires: sigcpp-toolfile
Requires: soqt-toolfile
Requires: sqlite-toolfile
Requires: systemtools
Requires: tauola-toolfile
Requires: thepeg-toolfile
Requires: toprex-toolfile
Requires: uuid-toolfile
Requires: xerces-c-toolfile
Requires: zlib-toolfile

%if "%isslc" == "true"
Requires: tkonlinesw-toolfile
Requires: gdb-toolfile
Requires: pyqt-toolfile
Requires: sip-toolfile
Requires: xrootd-toolfile
Requires: simage-toolfile
Requires: xdaq-toolfile
Requires: dcap-toolfile
Requires: frontier_client-toolfile
Requires: rulechecker-toolfile
Requires: curl-toolfile
Requires: valgrind-toolfile
Requires: google-perftools-toolfile
Requires: cmsswdata-toolfile
Requires: graphviz-toolfile
Requires: igprof-toolfile
%endif

%define is64bit %(case %cmsos in slc*_amd64%closingbrace echo true;; *%closingbrace echo false;; esac)
%if "%is64bit-%isslc" == "true-true"
Requires: libunwind-toolfile
%endif

%define skipreqtools jcompiler lhapdfwrapfull lhapdffull

## IMPORT scramv1-tool-conf
