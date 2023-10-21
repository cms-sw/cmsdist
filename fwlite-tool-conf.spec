### RPM cms fwlite-tool-conf 20.0
# with cmsBuild, change the above version only when a new
# tool is added
## INITENV SET CMSSW_TOOL_CONF_ROOT $FWLITE_TOOL_CONF_ROOT

Requires: eigen
Requires: fmt
Requires: tbb
Requires: boost
Requires: bz2lib
Requires: clhep
Requires: db6
Requires: dcap
Requires: expat
Requires: fakesystem
Requires: fftw3
Requires: fwlitedata
Requires: gcc
Requires: gdbm
Requires: gmake
Requires: gsl
Requires: hepmc
Requires: hepmc3
Requires: hls
Requires: libjpeg-turbo
Requires: libpng
Requires: libtiff
Requires: libungif
Requires: pcre
Requires: python3
Requires: root
Requires: sigcpp
Requires: sqlite
Requires: libuuid
Requires: xerces-c
Requires: xrootd
Requires: xz
Requires: zlib
Requires: libxml2
Requires: llvm
Requires: vdt
Requires: tinyxml2
Requires: md5
Requires: davix
Requires: py3-numpy
Requires: OpenBLAS
Requires: py3-pybind11
Requires: fwlite_python_tools
Requires: zstd
Requires: utm

# Only for Darwin platform.
%ifarch darwin
Requires: freetype
%endif

## INCLUDE cmssw-drop-tools
## INCLUDE scram-tool-conf
