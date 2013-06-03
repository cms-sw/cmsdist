### RPM cms iguana IGUANA_6_15_1-cms147a
## IMPORT configurations

Provides: /bin/zsh
Requires: iguana-tool-conf python cms-env
%define toolconf ${IGUANA_TOOL_CONF_ROOT}/configurations/tools-STANDALONE.conf
%define cvsdir iguana
%define cvsserver iguana
%define confversion %cmsConfiguration 
%define conflevel	_1
%define buildtarget release-build

# here cut and paste cms-scram-build.file
# I need to modify the cvs repo, since ignominy has been migrated to IT (SFA, 031106)

%define cvsproj     %(echo %n | sed -e "s|-debug||"| tr 'a-z' 'A-Z')
%define cvsrepo		cvs://:pserver:anonymous@isscvs.cern.ch:/local/reps/%cvsdir?passwd=AA_:yZZ3e
%define cvstag		%(echo %v | cut -d- -f1)
%if "%{?cvsconfig:set}" != "set"
%define cvsconfig	config
%endif
%define cvssrc		%cvsproj
%define srctree		src
%define tbxrepo		cvs://:pserver:anonymous@isscvs.cern.ch:/local/reps/scramtoolbox?passwd=AA_:yZZ3e
%define conftag		CMS_%confversion%conflevel
%define confsite	CMSconfigs

%if "%{buildarch:set}" != "set"
%define buildarch	:
%endif

%if "%{?buildtarget:set}" != "set"
%define buildtarget %{nil}	
%endif

# end cut and paste
## IMPORT scramv1-build




