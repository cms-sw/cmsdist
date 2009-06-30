### RPM cms online CMSSW_3_1_0_pre11_ONLINE
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

Requires: online-tool-conf python
Patch0: online_src

%define cmssw_release   %(perl -e '$_="%v"; s/_ONLINE//; print;')
%define cvsprojuc       %(echo %n | sed -e "s|-debug||"| tr 'a-z' 'A-Z')
%define cvsprojlc       %(echo %cvsprojuc | tr 'A-Z' 'a-z')
%define cvsdir          %cvsprojuc
%define cvsserver       %cvsprojlc
%define useCmsTC        1
%define buildtarget     release-build
%define saveDeps        yes

#Defines for file containing list of packages for checkout and build:
%define buildsetfile    online_build_set

%define patchsrc2	perl -p -i -e ' s!(<classpath.*/test\\+.*>)!!' config/BuildFile.xml
%define patchsrc3       %patch -p0

## IMPORT cms-scram-build
## IMPORT partial-build
## IMPORT scramv1-build
