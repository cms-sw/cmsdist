### RPM cms fwlite CMSSW_2_0_0_pre7_FWLITE
## IMPORT configurations 
Provides: /bin/zsh
Provides: /bin/sed
Provides: perl(Date::Format)
Provides: perl(Term::ReadKey)
Provides: perl(full)
Requires: fwlite-tool-conf python

%define cmssw_release   %(perl -e '$_="%v"; s/_FWLITE//; print;')
%define cvsprojuc       %(echo %n | sed -e "s|-debug||"| tr 'a-z' 'A-Z')
%define cvsprojlc       %(echo %cvsprojuc | tr 'A-Z' 'a-z')
%define cvsdir          %cvsprojuc
%define cvsserver       %cvsprojlc
%define buildtarget     release-build
%define saveDeps        yes

#Defines for file containing list of packages for checkout and build:
%define buildsetrepo    CMSDIST
%define buildsetfile    fwlite_build_set.file
%define buildsetvers    buildset_V3_5

# Skip library load and symbol checks to avoid dependency on seal:
%define nolibchecks     on

# Switch off building tests:
%define patchsrc3 perl -p -i -e ' s|(<classpath.*test\\+test.*>)||;' config/BuildFile.xml*


## IMPORT cms-scram-build
## IMPORT partial-build
## IMPORT scramv1-build
