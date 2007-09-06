### RPM cms oracle-env 1.7
## INITENV +PATH SQLPATH %i/etc
## INITENV SET TNS_ADMIN %i/etc

Source0: http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/*checkout*/COMP/PHEDEX/Schema/login.sql?rev=1.2&cvsroot=CMSSW
Source1: http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/*checkout*/COMP/PHEDEX/Schema/tnsnames.ora?rev=1.26&cvsroot=CMSSW
%prep
%build
%install
mkdir -p %i/etc
cp %_sourcedir/tnsnames.ora* %i/etc/tnsnames.ora
cp %_sourcedir/login.sql* %i/etc/login.sql
