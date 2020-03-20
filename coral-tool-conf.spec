### RPM cms coral-tool-conf 2.1
## NOCOMPILER

Requires: pcre-toolfile
Requires: python-toolfile
Requires: expat-toolfile
Requires: boost-toolfile
Requires: frontier_client-toolfile
Requires: gcc-toolfile
Requires: openssl-toolfile

Requires: sqlite-toolfile
Requires: libuuid-toolfile
Requires: zlib-toolfile
Requires: bz2lib-toolfile
Requires: cppunit-toolfile
Requires: xerces-c-toolfile
Requires: systemtools
%ifarch x86_64
Requires: oracle-toolfile
%endif

%define skipreqtools jcompiler

## IMPORT scramv1-tool-conf
