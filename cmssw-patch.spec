### RPM cms cmssw-patch CMSSW_3_6_1_patch5
## IMPORT configurations 

Requires: cmssw-patch-tool-conf 

%define cvsprojuc       %(echo %n | sed -e "s|-patch.*||"| tr 'a-z' 'A-Z')
%define cvsprojlc       %(echo %cvsprojuc | tr 'A-Z' 'a-z')
%define cvsdir          %cvsprojuc
%define cvssrc          %cvsprojuc
%define cvsserver       cmssw
%define cvsrep		cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/%cvsdir?passwd=AA_:yZZ3e
# %define cvsrepo		cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/%cvsdir?passwd=AA_:yZZ3e
%define useCmsTC        1

%define ucprojname      %cvsprojuc

%define prebuildtarget  gindices
%define buildtarget     release-build
%define saveDeps        yes

%define isPatch         yes

## IMPORT cms-scram-build
## IMPORT scramv1-patch-build
