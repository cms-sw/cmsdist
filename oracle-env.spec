### RPM cms oracle-env 29
## NOCOMPILER
## INITENV +PATH SQLPATH %i/etc
## INITENV SET TNS_ADMIN %i/etc

Source0: http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/*checkout*/COMP/PHEDEX/Schema/login.sql?rev=1.2&cvsroot=CMSSW
Source1: http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/*checkout*/COMP/PHEDEX/Schema/tnsnames.ora?rev=1.45&cvsroot=CMSSW
Source2: http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/*checkout*/COMP/PHEDEX/Schema/sqlnet.ora?rev=1.1&cvsroot=CMSSW
%prep
%build
%install
mkdir -p %i/etc
cp %_sourcedir/sqlnet.ora* %i/etc/sqlnet.ora
cp %_sourcedir/tnsnames.ora* %i/etc/tnsnames.ora
cp %_sourcedir/login.sql* %i/etc/login.sql
