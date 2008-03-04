<<<<<<< cmssw.spec
### RPM cms cmssw CMSSW_2_0_0_pre4
=======
### RPM cms cmssw CMSSW_1_8_0
>>>>>>> 1.288
## IMPORT configurations 
Provides: /bin/zsh
Provides: /bin/sed
Provides: perl(Date::Format)
Provides: perl(Term::ReadKey)
Provides: perl(full)
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
