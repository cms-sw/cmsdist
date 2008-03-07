### RPM cms coral-tool-conf CMS_151l

%if "%{?use_system_gcc:set}" != "set"
Requires: gcc
%endif

Requires: pcre
Requires: bz2lib
Requires: uuid
Requires: python
Requires: expat
Requires: gccxml
Requires: boost
Requires: gsl
Requires: clhep
Requires: root
Requires: castor
Requires: libjpg
Requires: dcap
Requires: oracle-env
Requires: frontier_client
Requires: sqlite
Requires: p5-dbd-oracle
Requires: seal

%if "%{?online_release:set}" != "set"
Requires: zlib
Requires: openssl
Requires: db4
Requires: gdbm
Requires: qt
Requires: mysql
Requires: libpng
Requires: oracle
Requires: libungif
Requires: libtiff
Requires: cppunit
Requires: xerces-c
Requires: systemtools
%endif

%if "%{?online_release:set}" == "set"
Requires: onlinesystemtools
%define onlinesystemtoolsroot ${ONLINESYSTEMTOOLS_ROOT}
%endif

%define skipreqtools %{nil}
%define skipreqtools jcompiler

## IMPORT scramv1-tool-conf
