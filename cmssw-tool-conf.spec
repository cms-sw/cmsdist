### RPM cms cmssw-tool-conf 57.0
# With cmsBuild, change the above version only when a new tool is added

## INSTALL_DEPENDENCIES cmsLHEtoEOSManager gcc-fixincludes cmssw-osenv cms-git-tools SCRAMV2
## UPLOAD_DEPENDENCIES dqmgui

Requires: AXOL1TL
Requires: CICADA
Requires: crab
Requires: cmssw-wm-tools
Requires: google-benchmark
Requires: catch2
Requires: starlight
Requires: alpgen
Requires: boost
Requires: bz2lib
Requires: cepgen
Requires: classlib
Requires: clhep
Requires: coral
Requires: cppunit
Requires: cpu_features
Requires: curl
Requires: das_client
Requires: db6
Requires: davix
Requires: evtgen
Requires: expat
Requires: fakesystem
Requires: flatbuffers
Requires: fmt
Requires: gbl
Requires: gcc
Requires: gdbm
Requires: geant4
Requires: geant4data
Requires: g4hepem
Requires: glimpse
Requires: gmake
Requires: gsl
Requires: highfive
Requires: hector
Requires: hepmc
Requires: hepmc3
Requires: heppdt
Requires: herwig7
Requires: hydjet
Requires: hydjet2
Requires: ittnotify
Requires: jemalloc
Requires: jemalloc-debug
Requires: jemalloc-prof
Requires: json
Requires: ktjet
Requires: lhapdf
Requires: libjpeg-turbo
Requires: libpng
Requires: libtiff
Requires: libungif
Requires: libxml2
Requires: lwtnn
Requires: meschach
Requires: pcre2
Requires: photospp
Requires: pyquen
Requires: pythia6
Requires: pythia8
Requires: python3
Requires: root
Requires: sherpa
Requires: libpciaccess
Requires: numactl
Requires: hwloc
Requires: gdrcopy
Requires: rdma-core
Requires: ucx
Requires: openmpi
Requires: sigcpp
Requires: sqlite
Requires: tauolapp
Requires: thepeg
Requires: libuuid
Requires: xerces-c
Requires: dcap
Requires: frontier_client
Requires: xrootd
Requires: xrdcl-record
Requires: dd4hep
Requires: valgrind
Requires: cmsswdata
Requires: zstd
Requires: hls
Requires: opencv
Requires: grpc
Requires: onnxruntime
Requires: triton-inference-client
Requires: hdf5
Requires: yaml-cpp
Requires: yoda
Requires: fftw3
Requires: fftjet
Requires: professor2
Requires: xz
Requires: lz4
Requires: protobuf
Requires: lcov
Requires: llvm
Requires: tbb
Requires: mctester
Requires: vdt
Requires: gnuplot
Requires: sloccount
Requires: millepede
Requires: pacparser
Requires: git
Requires: gmp-static
Requires: mpfr-static
Requires: fastjet-contrib
Requires: opencl
Requires: opencl-cpp
Requires: qd
Requires: blackhat
Requires: sherpa
Requires: fasthadd
Requires: eigen
Requires: gdb
Requires: libxslt
Requires: giflib
Requires: freetype
Requires: utm
Requires: libffi
Requires: CSCTrackFinderEmulation
Requires: tinyxml2
Requires: md5
Requires: gosamcontrib
Requires: gosam
Requires: madgraph5amcatnlo
Requires: python_tools
Requires: dasgoclient
Requires: dablooms

# Only for Linux platform.
%ifos linux
Requires: openldap
Requires: gperftools
Requires: cuda
Requires: cuda-compatible-runtime
Requires: alpaka

%if "%{cmsos}" != "slc7_aarch64"
Requires: cudnn
%endif

Requires: libunwind
%ifnarch ppc64le
Requires: igprof
Requires: openloops
%endif

%ifarch x86_64
Requires: tkonlinesw
Requires: oracle
Requires: icc
Requires: icx
Requires: intel-vtune
Requires: rocm
Requires: rocm-rocrand
Requires: cmsmon-tools
Requires: dip
%else
Requires: tkonlinesw-fake
Requires: oracle-fake
%endif
%endif

Requires: xtensor
Requires: xtl
Requires: xgboost

## INCLUDE cmssw-vectorization
## INCLUDE cmssw-drop-tools
## INCLUDE scram-tool-conf
