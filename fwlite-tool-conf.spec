### RPM cms fwlite-tool-conf 8.2
## NOCOMPILER
# with cmsBuild, change the above version only when a new
# tool is added
## INITENV SET CMSSW_TOOL_CONF_ROOT $FWLITE_TOOL_CONF_ROOT

Provides: libboost_regex-gcc-mt.so 
Provides: libboost_signals-gcc-mt.so 
Provides: libboost_thread-gcc-mt.so

Requires: boost-toolfile
Requires: bz2lib-toolfile
Requires: castor-toolfile
Requires: clhep-toolfile
Requires: db4-toolfile
Requires: dcap-toolfile
Requires: elementtree-toolfile
Requires: expat-toolfile
Requires: fakesystem
Requires: fftw3-toolfile
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
Requires: openldap-toolfile
Requires: openssl-toolfile
Requires: pcre-toolfile
Requires: python-ldap-toolfile
Requires: python-toolfile
Requires: roofit-toolfile
Requires: root-toolfile
Requires: sigcpp-toolfile
Requires: sqlite-toolfile
Requires: systemtools
Requires: uuid-toolfile
Requires: xrootd-toolfile
Requires: zlib-toolfile

%define skipreqtools jcompiler

## IMPORT scramv1-tool-conf
