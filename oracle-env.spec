### RPM cms oracle-env 1.0
## INITENV +PATH SQL_PATH %i/etc
## INITENV SET TNS_ADMIN %i/etc

Source0: http://cmsdoc.cern.ch/swdev/viewcvs/viewcvs.cgi/*checkout*/COMP/PHEDEX/Schema/login.sql?rev=1.1&cvsroot=CMSSW
Source1: http://cmsdoc.cern.ch/swdev/viewcvs/viewcvs.cgi/*checkout*/COMP/PHEDEX/Schema/tnsnames.ora?rev=1.17&cvsroot=CMSSW
%prep
%build
%install
cp %_sourcedir/tnsnames.ora* %i/etc/tnsnames.ora
cp %_sourcedir/login.sql* %i/etc/login.sql
