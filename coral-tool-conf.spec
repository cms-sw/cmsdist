### RPM cms coral-tool-conf 2.1
## NOCOMPILER
%define isnotonline %(case %{cmsplatf} in (*onl_*_*) echo 0 ;; (*) echo 1 ;; esac)
%define isamd64 %(case %{cmsplatf} in (*amd64*) echo 1 ;; (*) echo 0 ;; esac)

Requires: pcre-toolfile
Requires: python-toolfile
Requires: expat-toolfile
Requires: boost-toolfile
Requires: frontier_client-toolfile
Requires: gcc-toolfile
Requires: openssl-toolfile
Requires: python2to3

%if %isnotonline
Requires: sqlite-toolfile
Requires: libuuid-toolfile
Requires: zlib-toolfile
Requires: bz2lib-toolfile
Requires: cppunit-toolfile
Requires: xerces-c-toolfile
%if %isamd64
Requires: oracle-toolfile
%endif
Requires: systemtools
%else
Requires: onlinesystemtools
%define onlinesystemtoolsroot ${ONLINESYSTEMTOOLS_ROOT}
%endif

%define skipreqtools jcompiler

## IMPORT scramv1-tool-conf
