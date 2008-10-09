### RPM cms coral-tool-conf 1.0
# with cmsBuild, change the above version only when a new
# tool is added
%if "%{?use_system_gcc:set}" != "set"
Requires: gcc-toolfile
Requires: gmake
%endif

Requires: gcc
Requires: pcre
Requires: zlib
Requires: bz2lib
Requires: uuid
Requires: python
Requires: expat
Requires: openssl
Requires: db4
Requires: gdbm
Requires: gccxml
Requires: boost
Requires: gsl
Requires: clhep
Requires: root
Requires: qt
Requires: castor
Requires: mysql
Requires: libpng
Requires: libjpg
Requires: dcap
Requires: oracle
Requires: oracle-env
Requires: libungif
Requires: libtiff
Requires: cppunit
Requires: frontier_client
Requires: sqlite
Requires: xerces-c
Requires: p5-dbd-oracle
Requires: systemtools
Requires: seal

%define skipreqtools %{nil}
%define skipreqtools jcompiler

## IMPORT scramv1-tool-conf
