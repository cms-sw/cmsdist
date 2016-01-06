### RPM cms cmssw-tool-conf 32.0
## NOCOMPILER
# With cmsBuild, change the above version only when a new
# tool is added

%define islinux %(case %{cmsos} in (slc*|fc*) echo 1 ;; (*) echo 0 ;; esac)
%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)
%define isamd64 %(case %{cmsplatf} in (*amd64*) echo 1 ;; (*) echo 0 ;; esac)
%define isslc %(case %{cmsplatf} in (slc*) echo 1 ;; (*) echo 0 ;; esac)

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
Requires: das_client-toolfile
Requires: db4-toolfile
Requires: dbs-client-toolfile
Requires: dpm-toolfile
Requires: davix-toolfile
Requires: evtgen-toolfile
Requires: expat-toolfile
Requires: fakesystem
Requires: fastjet-toolfile
Requires: gcc-toolfile
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
Requires: openssl-toolfile
Requires: oracle-env
Requires: pcre-toolfile
Requires: photos-toolfile
Requires: photospp-toolfile
Requires: pythia6-toolfile
Requires: pythia8-toolfile
Requires: python-toolfile
Requires: qt-toolfile
Requires: root-toolfile
Requires: sherpa-toolfile
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
Requires: frontier_client-toolfile
Requires: xrootd-toolfile
Requires: pyqt-toolfile
Requires: sip-toolfile
Requires: graphviz-toolfile
Requires: valgrind-toolfile
Requires: py2-matplotlib-toolfile
Requires: py2-numpy-toolfile
Requires: py2-pandas-toolfile
Requires: py2-scipy-toolfile
Requires: cmsswdata-toolfile
Requires: py2-cjson-toolfile
Requires: py2-pycurl-toolfile
Requires: py2-sqlalchemy-toolfile
Requires: py2-pygithub-toolfile
Requires: py2-networkx-toolfile
Requires: py2-dablooms-toolfile
Requires: py2-dxr-toolfile
Requires: py2-futures-toolfile
Requires: py2-jinja-toolfile
Requires: py2-markupsafe-toolfile
Requires: py2-ordereddict-toolfile
Requires: py2-parsimonious-toolfile
Requires: py2-pygments-toolfile
Requires: py2-pysqlite-toolfile
Requires: py2-PyYAML-toolfile
Requires: py2-docopt-toolfile
Requires: py2-prettytable-toolfile
Requires: py2-schema-toolfile
Requires: rivet-toolfile
Requires: cascade-toolfile
Requires: cython-toolfile
Requires: yoda-toolfile
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
Requires: millepede-toolfile
Requires: cvs2git-toolfile
Requires: pacparser-toolfile
Requires: git-toolfile
Requires: cgal-toolfile
Requires: doxygen-toolfile
Requires: py2-python-dateutil-toolfile
Requires: yaml-cpp-toolfile
Requires: gmp-static-toolfile
Requires: mpfr-static-toolfile
Requires: fastjet-contrib-toolfile
Requires: cuda-toolfile
Requires: opencl-toolfile
Requires: opencl-cpp-toolfile
Requires: qd-toolfile
Requires: blackhat-toolfile
Requires: sherpa-toolfile
Requires: geant4-parfullcms-toolfile
Requires: fasthadd
Requires: eigen-toolfile
Requires: gdb-toolfile
Requires: py2-pytz-toolfile
Requires: file-toolfile
Requires: libxslt-toolfile
Requires: py2-six-toolfile
Requires: py2-pyparsing-toolfile
Requires: py2-requests-toolfile
Requires: giflib-toolfile
Requires: starlight-toolfile

# Only for Linux platform.
%if %islinux
Requires: openldap-toolfile
Requires: python-ldap-toolfile
Requires: google-perftools-toolfile
Requires: dmtcp-toolfile
%endif

# Only for Darwin platform.
%if %isdarwin
Requires: freetype-toolfile
%endif

# Only for INTEL/AMD platforms.
%if %isamd64
Requires: tkonlinesw-toolfile
Requires: py2-cx-oracle-toolfile
Requires: oracle-toolfile

# Only for slc platforms.
%if %isslc
Requires: openloops-toolfile
%endif

# Only for Linux platform.
%if %islinux
Requires: igprof-toolfile
Requires: glibc-toolfile
%endif
%endif

%define skipreqtools jcompiler icc-cxxcompiler icc-ccompiler icc-f77compiler cuda rivet2 opencl opencl-cpp

## IMPORT scramv1-tool-conf

