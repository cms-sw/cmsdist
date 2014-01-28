### RPM cms oracle-env 29
## NOCOMPILER
## INITENV +PATH SQLPATH %i/etc
## INITENV SET TNS_ADMIN %i/etc

Source0: http://cvs.web.cern.ch/cvs/cgi-bin/viewcvs.cgi/COMP/PHEDEX/Schema/login.sql?revision=1.2
Source1: http://cvs.web.cern.ch/cvs/cgi-bin/viewcvs.cgi/COMP/PHEDEX/Schema/tnsnames.ora?revision=1.45
Source2: http://cvs.web.cern.ch/cvs/cgi-bin/viewcvs.cgi/COMP/PHEDEX/Schema/sqlnet.ora?revision=1.1
Patch0: oracle-env-online
%prep
%build
%install
mkdir -p %i/etc
cp %_sourcedir/sqlnet.ora* %i/etc/sqlnet.ora
cp %_sourcedir/tnsnames.ora* %i/etc/tnsnames.ora
cp %_sourcedir/login.sql* %i/etc/login.sql
cd %i/etc
patch -p0 <%_sourcedir/oracle-env-online
