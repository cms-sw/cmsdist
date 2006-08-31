### RPM cms oracle-env 1.1
## INITENV +PATH SQLPATH %i/etc
## INITENV SET TNS_ADMIN %i/etc

Source0: http://cmsdoc.cern.ch/swdev/viewcvs/viewcvs.cgi/*checkout*/COMP/PHEDEX/Schema/login.sql?rev=1.1&cvsroot=CMSSW
Source1: http://cmsdoc.cern.ch/swdev/viewcvs/viewcvs.cgi/*checkout*/COMP/PHEDEX/Schema/tnsnames.ora?rev=1.20&cvsroot=CMSSW
%prep
%build
%install
mkdir -p %i/etc
cp %_sourcedir/tnsnames.ora* %i/etc/tnsnames.ora
cp %_sourcedir/login.sql* %i/etc/login.sql
