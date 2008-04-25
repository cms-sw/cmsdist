### RPM cms coral-tool-conf 1.0-204onl1
# with cmsBuild, change the above version only when a new
# tool is added
Requires: gmake
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
Requires: frontier_client
Requires: sqlite
Requires: p5-dbd-oracle
Requires: seal
Requires: libtiff
Requires: oracle-env


%if "%{?online_release:set}" != "set"

Requires: gcc-toolfile
Requires: gcc
Requires: zlib
Requires: openssl
Requires: db4
Requires: gdbm
Requires: qt
Requires: mysql
Requires: libpng
Requires: oracle
Requires: libungif
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
