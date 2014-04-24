### RPM cms fwlite-tool-conf 9.0
## NOCOMPILER
# with cmsBuild, change the above version only when a new
# tool is added
## INITENV SET CMSSW_TOOL_CONF_ROOT $FWLITE_TOOL_CONF_ROOT

Provides: libboost_regex-gcc-mt.so 
Provides: libboost_signals-gcc-mt.so 
Provides: libboost_thread-gcc-mt.so

Requires: tbb-toolfile
Requires: boost-toolfile
Requires: bz2lib-toolfile
Requires: castor-toolfile
Requires: clhep-toolfile
Requires: db4-toolfile
Requires: dcap-toolfile
Requires: expat-toolfile
Requires: fakesystem
Requires: fftw3-toolfile
# Use our own freetype only on macosx.
%if "%(case %cmsplatf in (osx*) echo true ;; (*) echo false ;; esac)" == "true"
Requires: freetype-toolfile
%endif
Requires: fwlitedata-toolfile
Requires: gcc-toolfile
Requires: gccxml-toolfile
Requires: gdbm-toolfile
Requires: gmake-toolfile
Requires: gsl-toolfile
Requires: hepmc-toolfile
Requires: libjpg-toolfile
Requires: libpng-toolfile
Requires: libtiff-toolfile
Requires: libungif-toolfile
Requires: openssl-toolfile
Requires: pcre-toolfile
Requires: python-toolfile
Requires: roofit-toolfile
Requires: root-toolfile
Requires: sigcpp-toolfile
Requires: sqlite-toolfile
Requires: systemtools
Requires: libuuid-toolfile
Requires: xrootd-toolfile
Requires: xz-toolfile
Requires: zlib-toolfile
Requires: libxml2-toolfile

%define skipreqtools jcompiler db4 expat fftw3 sqlite

## IMPORT scramv1-tool-conf
