### RPM cms cmssw-patch CMSSW_2_1_10_patch1
## IMPORT configurations 
Provides: /bin/zsh
Provides: /bin/ksh
Provides: /bin/sed
Provides: /usr/bin/awk
Provides: /usr/bin/python
Provides: perl(Date::Format)
Provides: perl(Term::ReadKey)
Provides: perl(full)
Provides: perl(LWP::UserAgent)
Provides: perl(Template)

Requires: cmssw-patch-tool-conf 

%define cvsprojuc       %(echo %n | sed -e "s|-patch.*||"| tr 'a-z' 'A-Z')
%define cvsprojlc       %(echo %cvsprojuc | tr 'A-Z' 'a-z')
%define cvsdir          %cvsprojuc
%define cvssrc          %cvsprojuc
%define cvsserver       cmssw
# %define cvsrepo		cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/%cvsdir?passwd=AA_:yZZ3e
%define useCmsTC        1

%define ucprojname      %cvsprojuc

%define prebuildtarget  gindices
%define buildtarget     release-build
%define saveDeps        yes

%define isPatch         yes

## IMPORT cms-scram-build
## IMPORT scramv1-patch-build
