### RPM cms coral-tool-conf 10.0

Requires: pcre
Requires: python3
Requires: expat
Requires: boost
Requires: frontier_client
Requires: gcc
Requires: sqlite
Requires: libuuid
Requires: zlib
Requires: bz2lib
Requires: cppunit
Requires: xerces-c
%ifarch x86_64
Requires: oracle
%endif

%define skipreqtools jcompiler

## INCLUDE scram-tool-conf
