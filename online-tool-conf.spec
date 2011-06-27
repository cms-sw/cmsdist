### RPM cms online-tool-conf 7.0
## NOCOMPILER
# with cmsBuild, change the above version only when a new
# tool is added

## INITENV SET CMSSW_TOOL_CONF_ROOT $ONLINE_TOOL_CONF_ROOT
Provides: libboost_regex-gcc-mt.so 
Provides: libboost_signals-gcc-mt.so 
Provides: libboost_thread-gcc-mt.so
%define closingbrace )
%define isslc %(case %cmsos in slc*%closingbrace echo true;; *%closingbrace echo false;; esac)
%define is64bit %(case %cmsos in slc*_amd64%closingbrace echo true;; *%closingbrace echo false;; esac)

#Requires: alpgen-toolfile                  # not used online
Requires: boost-toolfile
Requires: bz2lib-toolfile
Requires: castor-toolfile
#Requires: charybdis-toolfile               # not used online
Requires: classlib-toolfile
Requires: clhep-toolfile
Requires: coral-toolfile
#Requires: cppunit-toolfile                 # not used online
#Requires: curl-toolfile                    # from SLC5 (curl)
#Requires: db4-toolfile                     # not used online
#Requires: dbs-client-toolfile              # not used online
#Requires: dpm-toolfile                     # not used online
Requires: elementtree-toolfile
#Requires: evtgenlhc-toolfile               # not used online
Requires: expat-toolfile
Requires: fakesystem
Requires: fastjet-toolfile
#Requires: gcc-toolfile                     # installed as system compiler
Requires: gccxml-toolfile
#Requires: gdbm-toolfile                    # not used online
#Requires: geant4-toolfile                  # not used online
#Requires: geant4data-toolfile              # not used online
#Requires: glimpse-toolfile                 # not used online
Requires: gmake-toolfile
Requires: gsl-toolfile
#Requires: hector-toolfile                  # not used online
Requires: hepmc-toolfile
Requires: heppdt-toolfile
#Requires: herwig-toolfile                  # not used online
#Requires: herwigpp-toolfile                # not used online
#Requires: jimmy-toolfile                   # not used online
Requires: ktjet-toolfile
#Requires: lhapdf-toolfile                  # not used online
#Requires: libhepml-toolfile                # not used online
Requires: libjpg-toolfile
Requires: libpng-toolfile
Requires: libtiff-toolfile
Requires: libungif-toolfile
#Requires: mcdb-toolfile                    # not used online
#Requires: meschach-toolfile                # not used online
#Requires: millepede-toolfile               # not used online
#Requires: mimetic-toolfile                 # from XDAQ (daq-mimetic)
#Requires: openldap-toolfile                # not used online
#Requires: openssl-toolfile                 # from SLC5 (openssl)
Requires: oracle-env
#Requires: oracle-toolfile                  # from XDAQ (daq-oracle)
Requires: pcre-toolfile
#Requires: photos-toolfile                  # not used online
#Requires: pythia6-toolfile                 # not used online
#Requires: pythia8-toolfile                 # not used online
#Requires: python-ldap-toolfile             # not used online
Requires: python-toolfile
#Requires: qt-toolfile                      # not used online
Requires: roofit-toolfile
Requires: root-toolfile
#Requires: sherpa-toolfile                  # not used online
Requires: sigcpp-toolfile
#Requires: sqlite-toolfile                  # from XDAQ (daq-sqlite)
Requires: onlinesystemtools
#Requires: tauola-toolfile                  # not used online
#Requires: thepeg-toolfile                  # not used online
#Requires: toprex-toolfile                  # not used online
#Requires: uuid-toolfile                    # from SLC5 (e2fsprogs-libs)
#Requires: xerces-c-toolfile                # from XDAQ (daq-xerces)
#Requires: zlib-toolfile                    # from SLC5 (zlib)
Requires: dcap-toolfile
#Requires: xdaq-toolfile                    # from XDAQ (daq-xdaq)
#Requires: tkonlinesw-toolfile              # not used online
Requires: frontier_client-toolfile
#Requires: xrootd-toolfile                  # not used online
#Requires: pyqt-toolfile                    # not used online
#Requires: sip-toolfile                     # not used online
#Requires: graphviz-toolfile                # not used online
Requires: valgrind-toolfile
#Requires: py2-matplotlib-toolfile          # not used online
#Requires: py2-numpy-toolfile               # not used online
Requires: cmsswdata-toolfile
#Requires: rivet-toolfile                   # not used online
#Requires: cascade-toolfile                 # not used online
Requires: fftw3-toolfile
#Requires: fftjet-toolfile                  # not used online
Requires: gdb-toolfile
#Requires: google-perftools-toolfile        # not used online
Requires: igprof-toolfile

%define skipreqtools jcompiler lhapdfwrapfull lhapdffull
%define onlinesystemtoolsroot ${ONLINESYSTEMTOOLS_ROOT}
## IMPORT scramv1-tool-conf
