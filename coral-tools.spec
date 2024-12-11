### RPM cms coral-tools 1.0

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
%define override_microarch -march=x86-64-v2
## INCLUDE scram/tool-conf-src
