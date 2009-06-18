### RPM cms coral-tool-conf 1.0
# with cmsBuild, change the above version only when a new tool is added
%define online %(case %cmsplatf in *onl_*_*) echo true ;; esac)
Requires: pcre
Requires: uuid
Requires: python
Requires: expat
Requires: boost
Requires: frontier_client
Requires: sqlite
Requires: oracle-env

%if "%online" != "true"
Requires: gcc-toolfile
Requires: gcc
Requires: zlib
Requires: openssl
Requires: cppunit
Requires: xerces-c
Requires: oracle
Requires: systemtools
%else
Requires: onlinesystemtools
%define onlinesystemtoolsroot ${ONLINESYSTEMTOOLS_ROOT}
%endif

%define skipreqtools %{nil}
%define skipreqtools jcompiler

## IMPORT scramv1-tool-conf
