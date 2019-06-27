### RPM cms fwlite-tool-conf 11.0
## NOCOMPILER
# with cmsBuild, change the above version only when a new
# tool is added
## INITENV SET CMSSW_TOOL_CONF_ROOT $FWLITE_TOOL_CONF_ROOT

%define isslc %(case %{cmsos} in (slc*) echo 1 ;; (*) echo 0 ;; esac)
%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)
%define isamd64 %(case %{cmsplatf} in (*amd64*) echo 1 ;; (*) echo 0 ;; esac)

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

%if %isamd64
%if %isslc
Requires: glibc-toolfile
%endif
%endif

# Only for Darwin platform.
%if %isdarwin
Requires: freetype-toolfile
%endif

%define skipreqtools jcompiler db6 expat fftw3 sqlite

## IMPORT scramv1-tool-conf
# bla bla
