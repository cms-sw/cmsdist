### RPM cms cmssw CMSSW_1_7_5_g491p1 
## IMPORT configurations 
Provides: /bin/zsh
Requires: cmssw-tool-conf python glimpse

%define cvsprojuc       %(echo %n | sed -e "s|-debug||"| tr 'a-z' 'A-Z')
%define cvsprojlc       %(echo %cvsprojuc | tr 'A-Z' 'a-z')
%define cvsdir          %cvsprojuc
%define cvsserver       %cvsprojlc
%define prebuildtarget  gindices
%define buildtarget     release-build
%define useCmsTC        1
%define saveDeps        yes

## IMPORT cms-scram-build
## IMPORT scramv1-build
