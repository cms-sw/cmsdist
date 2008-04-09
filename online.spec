### RPM cms online CMSSW_2_0_0_pre7_ONLINE1
## IMPORT configurations 
Provides: /bin/zsh
Provides: /bin/sed
Provides: perl(Date::Format)
Provides: perl(Term::ReadKey)
Provides: perl(full)
Requires: online-tool-conf python

%define cmssw_release   %(perl -e '$_="%v"; s/_ONLINE1//; print;')
%define cvsprojuc       %(echo %n | sed -e "s|-debug||"| tr 'a-z' 'A-Z')
%define cvsprojlc       %(echo %cvsprojuc | tr 'A-Z' 'a-z')
%define cvsdir          %cvsprojuc
%define cvsserver       %cvsprojlc
%define buildtarget     release-build
%define saveDeps        yes

#Defines for file containing list of packages for checkout and build:
%define buildsetrepo    CMSDIST
%define buildsetfile    online_build_set.file
%define buildsetvers    buildset_V1_0


%define patchsrc2     perl -p -i -e ' s!(<classpath.*/test\\+.*>)!!;' config/BuildFile.xml
%define patchsrc3     perl -p -i -e ' s!int depth=1,!int depth,!;' src/DQM/HcalMonitorTasks/interface/HcalTrigPrimMonitor.h

## IMPORT cms-scram-build
## IMPORT partial-build
## IMPORT scramv1-build
