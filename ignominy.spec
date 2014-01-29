### RPM cms ignominy IGNOMINY_4_7_0-CMS18
## IMPORT configurations

Provides: /bin/zsh
Requires: ignominy-tool-conf rulechecker
%define cvsprojuc       %(echo %n | sed -e "s|-debug||"| tr 'a-z' 'A-Z')
%define cvsprojlc       %(echo %cvsprojuc | tr 'A-Z' 'a-z')
%define cvsdir          %cvsprojlc
%define cvsserver       %cvsprojlc
%define buildtarget     release-build
%define postbuildtarget doc
%define cvsrepo		cvs://:pserver:anonymous@isscvs.cern.ch:/local/reps/%cvsdir?passwd=AA_:yZZ3e

## IMPORT cms-scram-build
## IMPORT scramv1-build
