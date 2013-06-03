### RPM cms pool-tool-conf 2.0
## NOCOMPILER
# with cmsBuild, change the above version only when a new tool is added
%define closingbrace )
%define online %(case %cmsplatf in *onl_*_*%closingbrace echo true;; *%closingbrace echo false;; esac)

Requires: pcre-toolfile
Requires: python-toolfile
Requires: expat-toolfile
Requires: gccxml-toolfile
Requires: boost-toolfile
Requires: root-toolfile
Requires: coral-toolfile
Requires: gcc-toolfile

%if "%online" != "true"
Requires: uuid-toolfile
Requires: zlib-toolfile
Requires: cppunit-toolfile
Requires: xerces-c-toolfile
Requires: systemtools
%else
Requires: onlinesystemtools
%define onlinesystemtoolsroot ${ONLINESYSTEMTOOLS_ROOT}
%endif

%define skipreqtools %{nil}
%define skipreqtools jcompiler

## IMPORT scramv1-tool-conf
