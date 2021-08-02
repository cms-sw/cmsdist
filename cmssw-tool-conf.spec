### RPM cms cmssw-tool-conf 50.0
# With cmsBuild, change the above version only when a new tool is added

## NOCOMPILER
## INSTALL_DEPENDENCIES cmsLHEtoEOSManager gcc-fixincludes cmssw-osenv cms-git-tools
## UPLOAD_DEPENDENCIES dqmgui

%define vectorized_packages OpenBLAS fastjet mkfit rivet tensorflow vecgeom zlib
%{expand:%(for t in %{vectorized_packages} ; do echo Requires: $t; for v in %{package_vectorization}; do echo Requires: ${t}_${v}; done; done)}

Requires: crab
Requires: cmssw-wm-tools
Requires: google-benchmark
Requires: catch2
Requires: starlight
Requires: alpgen
Requires: boost
Requires: bz2lib
Requires: charybdis
Requires: classlib
Requires: clhep
Requires: coral
Requires: cppunit
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
Requires: glimpse
Requires: gmake
Requires: gsl
Requires: highfive
Requires: hector
Requires: hepmc
Requires: heppdt
Requires: herwig
Requires: herwig7
Requires: hydjet
Requires: ittnotify
Requires: jemalloc
Requires: jemalloc-debug
Requires: jimmy
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
Requires: pcre
Requires: photos
Requires: photospp
Requires: pyquen
Requires: pythia6
Requires: pythia8
Requires: python
Requires: python3
Requires: root
Requires: sherpa
Requires: libpciaccess
Requires: numactl
Requires: hwloc
Requires: gdrcopy
Requires: ucx
Requires: openmpi
Requires: sigcpp
Requires: sqlite
Requires: tauola
Requires: tauolapp
Requires: thepeg
Requires: toprex
Requires: libuuid
Requires: xerces-c
Requires: dcap
Requires: frontier_client
Requires: xrootd
Requires: dd4hep
Requires: graphviz
Requires: valgrind
Requires: cmsswdata
Requires: zstd
Requires: hls
Requires: opencv
Requires: grpc
Requires: onnxruntime
Requires: triton-inference-client
Requires: hdf5
Requires: cascade
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
Requires: icc
Requires: gnuplot
Requires: sloccount
Requires: millepede
Requires: pacparser
Requires: git
Requires: cgal
Requires: doxygen
Requires: yaml-cpp
Requires: gmp-static
Requires: mpfr-static
Requires: fastjet-contrib
Requires: opencl
Requires: opencl-cpp
Requires: qd
Requires: blackhat
Requires: sherpa
Requires: geant4-parfullcms
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
Requires: mxnet-predict
Requires: dablooms
Requires: oracle
Requires: tkonlinesw

# Only for Linux platform.
%ifos linux
Requires: openldap
Requires: gperftools
Requires: cuda
Requires: alpaka
Requires: cupla

%if "%{cmsos}" != "slc7_aarch64"
Requires: cudnn
%endif

Requires: libunwind
%ifnarch ppc64le
Requires: igprof
Requires: openloops
%endif

%ifarch x86_64
Requires: dmtcp
Requires: intel-vtune
Requires: cmsmon-tools
Requires: dip
%endif
%endif

Requires: xtensor
Requires: xtl
Requires: xgboost

%define skipreqtools jcompiler icc-cxxcompiler icc-ccompiler icc-f77compiler rivet2 opencl opencl-cpp nvidia-drivers intel-vtune jemalloc-debug

## INCLUDE scram-tool-conf
