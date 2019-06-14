### RPM cms cmssw-tool-conf 45.0
## NOCOMPILER
# With cmsBuild, change the above version only when a new tool is added

%define islinux %(case $(uname -s) in (Linux) echo 1 ;; (*) echo 0 ;; esac)
%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)
%define isamd64 %(case %{cmsplatf} in (*amd64*) echo 1 ;; (*) echo 0 ;; esac)
%define isslc %(case %{cmsplatf} in (slc*) echo 1 ;; (*) echo 0 ;; esac)
%define isnotppc64le %(case %{cmsplatf} in (*_ppc64le_*) echo 0 ;; (*) echo 1 ;; esac)
%define isnotppc64le_be %(case %{cmsplatf} in (*_ppc64*) echo 0 ;; (*) echo 1 ;; esac)
%define isnotaarch64 %(case %{cmsplatf} in (*_aarch64_*) echo 0 ;; (*) echo 1 ;; esac)
%define isslc7 %(case %{cmsplatf} in (slc7_amd64*) echo 1 ;; (*) echo 0 ;; esac)

Requires: google-benchmark-toolfile
Requires: catch2-toolfile
Requires: starlight-toolfile
Requires: alpgen-toolfile
Requires: boost-toolfile
Requires: bz2lib-toolfile
Requires: charybdis-toolfile
Requires: classlib-toolfile
Requires: clhep-toolfile
Requires: coral-toolfile
Requires: cppunit-toolfile
Requires: curl-toolfile
Requires: das_client-toolfile
Requires: db6-toolfile
Requires: dpm-toolfile
Requires: davix-toolfile
Requires: evtgen-toolfile
Requires: expat-toolfile
Requires: fakesystem
Requires: fastjet-toolfile
Requires: gbl-toolfile
Requires: gcc-toolfile
Requires: gdbm-toolfile
Requires: geant4-toolfile
Requires: geant4data-toolfile
Requires: vecgeom-toolfile
Requires: glimpse-toolfile
Requires: gmake-toolfile
Requires: gsl-toolfile
Requires: hector-toolfile
Requires: hepmc-toolfile
Requires: heppdt-toolfile
Requires: herwig-toolfile
Requires: herwigpp-toolfile
Requires: ittnotify-toolfile
Requires: jemalloc-toolfile
Requires: jemalloc-debug-toolfile
Requires: jimmy-toolfile
Requires: ktjet-toolfile
Requires: lhapdf-toolfile
Requires: libhepml-toolfile
Requires: libjpeg-turbo-toolfile
Requires: libpng-toolfile
Requires: libtiff-toolfile
Requires: libungif-toolfile
Requires: libxml2-toolfile
Requires: lwtnn-toolfile
Requires: mcdb-toolfile
Requires: meschach-toolfile
Requires: openssl-toolfile
Requires: pcre-toolfile
Requires: photos-toolfile
Requires: photospp-toolfile
Requires: pyquen-toolfile
Requires: pythia6-toolfile
Requires: pythia8-toolfile
Requires: vincia-toolfile
Requires: dire-toolfile
Requires: python-toolfile
Requires: python3-toolfile
Requires: qt-toolfile
Requires: root-toolfile
Requires: sherpa-toolfile
Requires: openmpi-toolfile
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
Requires: dd4hep-toolfile
%if %isnotaarch64
Requires: pyqt-toolfile
%endif
Requires: sip-toolfile
Requires: graphviz-toolfile
Requires: valgrind-toolfile
Requires: cmsswdata-toolfile
Requires: zstd-toolfile

Requires: hdf5-toolfile
Requires: rivet-toolfile
Requires: cascade-toolfile
Requires: yoda-toolfile
Requires: fftw3-toolfile
Requires: fftjet-toolfile
Requires: lapack-toolfile
Requires: pyminuit2-toolfile
Requires: professor-toolfile
Requires: professor2-toolfile
Requires: xz-toolfile
Requires: protobuf-toolfile
Requires: lcov-toolfile
Requires: llvm-gcc-toolfile
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
Requires: yaml-cpp-toolfile
Requires: gmp-static-toolfile
Requires: mpfr-static-toolfile
Requires: fastjet-contrib-toolfile
Requires: opencl-toolfile
Requires: opencl-cpp-toolfile
Requires: qd-toolfile
Requires: blackhat-toolfile
Requires: sherpa-toolfile
Requires: geant4-parfullcms-toolfile
Requires: fasthadd
Requires: eigen-toolfile
Requires: gdb-toolfile
Requires: libxslt-toolfile
Requires: giflib-toolfile
Requires: freetype-toolfile
Requires: utm-toolfile
Requires: libffi-toolfile
Requires: CSCTrackFinderEmulation-toolfile
Requires: tinyxml2-toolfile
Requires: scons-toolfile
Requires: md5-toolfile
Requires: gosamcontrib-toolfile
Requires: gosam-toolfile
Requires: madgraph5amcatnlo-toolfile
Requires: geneva-toolfile
Requires: python_tools
Requires: dasgoclient
Requires: OpenBLAS-toolfile
Requires: mxnet-predict-toolfile

# Only for Linux platform.
%if %islinux
Requires: codechecker-toolfile
Requires: gcc-checker-plugin-toolfile
Requires: openldap-toolfile
Requires: gperftools-toolfile

%if %isnotppc64le_be
Requires: igprof-toolfile
Requires: cuda-toolfile
Requires: cub-toolfile
Requires: cuda-api-wrappers-toolfile
Requires: openloops-toolfile
%endif

%if %isamd64
Requires: dmtcp-toolfile
Requires: tkonlinesw-toolfile
Requires: oracle-toolfile
Requires: intel-vtune

%if %isslc
Requires: glibc-toolfile
%endif
%else
Requires: tkonlinesw-fake-toolfile
Requires: oracle-fake-toolfile
%endif
%endif

Requires: tensorflow-toolfile
Requires: xtensor-toolfile
Requires: xtl-toolfile

%define skipreqtools jcompiler icc-cxxcompiler icc-ccompiler icc-f77compiler rivet2 opencl opencl-cpp nvidia-drivers intel-vtune jemalloc-debug

## IMPORT scramv1-tool-conf

