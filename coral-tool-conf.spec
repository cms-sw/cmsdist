### RPM cms coral-tool-conf 2.1
## NOCOMPILER
# with cmsBuild, change the above version only when a new tool is added
%define closingbrace )
%define online %(case %cmsplatf in *onl_*_*%closingbrace echo true;; *%closingbrace echo false;; esac)
Requires: pcre-toolfile
Requires: python-toolfile
Requires: expat-toolfile
Requires: boost-toolfile
Requires: frontier_client-toolfile
Requires: gcc-toolfile
Requires: openssl-toolfile

%if "%online" != "true"
Requires: sqlite-toolfile
Requires: libuuid-toolfile
Requires: zlib-toolfile
Requires: cppunit-toolfile
Requires: xerces-c-toolfile
Requires: oracle-toolfile
Requires: systemtools
%else
Requires: onlinesystemtools
%define onlinesystemtoolsroot ${ONLINESYSTEMTOOLS_ROOT}
%endif

%define skipreqtools jcompiler

## IMPORT scramv1-tool-conf
