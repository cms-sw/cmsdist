### RPM cms cmssw-tool-conf 27.1
## NOCOMPILER
# with cmsBuild, change the above version only when a new
# tool is added

%define isslc %(case %cmsos in (slc*) echo true;; (*) echo false;; esac)
%define isslc6 %(case %cmsos in (slc6*) echo true ;; (*) echo false ;; esac)

Requires: alpgen-toolfile
Requires: boost-toolfile
Requires: bz2lib-toolfile
Requires: castor-toolfile
Requires: charybdis-toolfile
Requires: classlib-toolfile
Requires: clhep-toolfile
Requires: coral-toolfile
Requires: cppunit-toolfile
Requires: curl-toolfile
# Use our own freetype only on macosx.
%if "%(case %cmsplatf in (osx*) echo true ;; (*) echo false ;; esac)" == "true"
Requires: freetype-toolfile
%endif
Requires: das-client-toolfile
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
Requires: geant4data-toolfile
Requires: glimpse-toolfile
Requires: gmake-toolfile
Requires: gsl-toolfile
Requires: hector-toolfile
Requires: hepmc-toolfile
Requires: heppdt-toolfile
Requires: herwig-toolfile
Requires: herwigpp-toolfile
Requires: jemalloc-toolfile
Requires: jimmy-toolfile
Requires: ktjet-toolfile
Requires: lhapdf-toolfile
Requires: libhepml-toolfile
Requires: libjpg-toolfile
Requires: libpng-toolfile
Requires: libtiff-toolfile
Requires: libungif-toolfile
Requires: libxml2-toolfile
Requires: mcdb-toolfile
Requires: meschach-toolfile
Requires: millepede-toolfile
Requires: mimetic-toolfile
Requires: openssl-toolfile
Requires: oracle-env
Requires: oracle-toolfile
Requires: pcre-toolfile
Requires: photos-toolfile
Requires: pythia6-toolfile
Requires: pythia8-toolfile
Requires: python-toolfile
Requires: py2-cx-oracle-toolfile
Requires: qt-toolfile
Requires: roofit-toolfile
Requires: root-toolfile
Requires: sigcpp-toolfile
Requires: sqlite-toolfile
Requires: systemtools
Requires: tauola-toolfile
Requires: tauolapp-toolfile
Requires: thepeg-toolfile
Requires: toprex-toolfile
Requires: libuuid-toolfile
Requires: xerces-c-toolfile
Requires: zlib-toolfile
Requires: dcap-toolfile
Requires: xdaq-toolfile
Requires: tkonlinesw-toolfile
Requires: frontier_client-toolfile
Requires: xrootd-toolfile
Requires: pyqt-toolfile
Requires: sip-toolfile
Requires: graphviz-toolfile
Requires: valgrind-toolfile
Requires: py2-matplotlib-toolfile
Requires: py2-numpy-toolfile
Requires: py2-scipy-toolfile
Requires: cmsswdata-toolfile
Requires: py2-cjson-toolfile
Requires: py2-pycurl-toolfile
Requires: py2-pygithub-toolfile
Requires: rivet-toolfile
Requires: cascade-toolfile
Requires: fftw3-toolfile
Requires: fftjet-toolfile
Requires: lapack-toolfile
Requires: pyminuit2-toolfile
Requires: professor-toolfile
Requires: py2-ipython-toolfile
Requires: xz-toolfile
Requires: protobuf-toolfile
Requires: lcov-toolfile
Requires: llvm-gcc-toolfile
Requires: py2-lint-toolfile
Requires: tbb-toolfile
Requires: mctester-toolfile
Requires: vdt-toolfile
Requires: icc-gcc-toolfile
Requires: ccache-gcc-toolfile
Requires: distcc-gcc-toolfile
Requires: gnuplot-toolfile
Requires: sloccount-toolfile
Requires: cvs2git-toolfile
Requires: pacparser-toolfile
Requires: git-toolfile
Requires: cuda-toolfile
Requires: opencl-toolfile
Requires: opencl-cpp-toolfile
Requires: qd-toolfile
Requires: blackhat-toolfile
Requires: sherpa-toolfile
Requires: eigen-toolfile
Requires: file-toolfile

%if "%isslc" == "true"
Requires: openldap-toolfile
Requires: python-ldap-toolfile
Requires: gdb-toolfile
Requires: google-perftools-toolfile
Requires: igprof-toolfile
%endif

%define skipreqtools jcompiler lhapdfwrapfull lhapdffull icc-cxxcompiler icc-ccompiler icc-f77compiler cuda opencl opencl-cpp

## IMPORT scramv1-tool-conf

