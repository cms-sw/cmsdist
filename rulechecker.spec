### RPM cms rulechecker 2.6-CMS19
## BUILDIF case $(uname):$(uname -p) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac     
## INITENV +PATH CLASSPATH %i:%i/reveng:%i/reveng/flowanalysis.jar
Source: http://eulisse.web.cern.ch/eulisse/RuleChecker-2.6CMSp1.tgz 
Provides: perl(+=)
Provides: perl(=)
%prep
%setup -n CMS2.6_p1
%build
%install
cp -r . %i
rm -rf %{i}/userConfig/ATLAS/ALICE
perl -p -i -e "s|#!.*perl|#!/usr/bin/env perl|" $(find %{i}/reveng %{i}/dyn %{i}/patch %{i}/man %{i}/webreveng)
