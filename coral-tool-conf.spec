### RPM cms coral-tool-conf CMS_150d
%if "%{?use_system_gcc:set}" != "set"
Requires: gcc
%endif

%if "%{?online_release:set}" != "set"
Requires: zlib
Requires: expat
Requires: openssl
Requires: db4
Requires: gdbm
Requires: qt
Requires: castor
Requires: mysql
Requires: libpng
Requires: libjpg
Requires: dcap
Requires: oracle
Requires: oracle-env
Requires: p5-dbd-oracle
Requires: libungif
Requires: libtiff
Requires: xerces-c
Requires: cppunit
%endif

Requires: python
Requires: pcre
Requires: bz2lib
Requires: uuid
Requires: gccxml
Requires: boost
Requires: gsl
Requires: clhep
Requires: root
Requires: systemtools
Requires: frontier_client
Requires: sqlite
Requires: seal

%define skipreqtools %{nil}
%define skipreqtools jcompiler

## IMPORT scramv1-tool-conf
