### RPM cms fwlite-tool-conf 11.0
## NOCOMPILER
# with cmsBuild, change the above version only when a new
# tool is added
## INITENV SET CMSSW_TOOL_CONF_ROOT $FWLITE_TOOL_CONF_ROOT

Requires: fmt-toolfile
Requires: tbb-toolfile
Requires: boost-toolfile
Requires: bz2lib-toolfile
Requires: clhep-toolfile
Requires: db6-toolfile
Requires: dcap-toolfile
Requires: expat-toolfile
Requires: fakesystem
Requires: fftw3-toolfile
Requires: fwlitedata-toolfile
Requires: gcc-toolfile
Requires: gdbm-toolfile
Requires: gmake-toolfile
Requires: gsl-toolfile
Requires: hepmc-toolfile
Requires: libjpeg-turbo-toolfile
Requires: libpng-toolfile
Requires: libtiff-toolfile
Requires: libungif-toolfile
Requires: openssl-toolfile
Requires: pcre-toolfile
Requires: python-toolfile
Requires: root-toolfile
Requires: sigcpp-toolfile
Requires: sqlite-toolfile
Requires: systemtools
Requires: libuuid-toolfile
Requires: xerces-c-toolfile
Requires: xrootd-toolfile
Requires: xz-toolfile
Requires: zlib-toolfile
Requires: libxml2-toolfile
Requires: llvm-gcc-toolfile
Requires: vdt-toolfile
Requires: tinyxml2-toolfile
Requires: md5-toolfile
Requires: davix-toolfile
Requires: py2-numpy-toolfile
Requires: OpenBLAS-toolfile
Requires: py2-pybind11-toolfile
Requires: fwlite_python_tools
Requires: zstd-toolfile

%ifarch x86_64
%ifos linux
Requires: glibc-toolfile
%endif
%endif

# Only for Darwin platform.
%ifarch darwin
Requires: freetype-toolfile
%endif

%define skipreqtools jcompiler db6 expat fftw3 sqlite

## IMPORT scramv1-tool-conf
