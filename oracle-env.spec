### RPM cms oracle-env 31
## NOCOMPILER
## INITENV +PATH SQLPATH %i/etc
## INITENV SET TNS_ADMIN %i/etc

Source0: https://raw.githubusercontent.com/dmwm/PHEDEX/83abd11c2b5e6a3da4f46714d95ce467f6098920/Schema/login.sql

# The following tnsnames.ora amd sqlnet.ora files were taken
# from their official, CERN provided copy in /afs/cern.ch/project/oracle/admin/
Source1: oracle-tnsnames.ora
Source2: oracle-sqlnet.ora

%prep
%build
%install
mkdir -p %i/etc
cp %_sourcedir/oracle-sqlnet.ora* %i/etc/sqlnet.ora
cp %_sourcedir/oracle-tnsnames.ora* %i/etc/tnsnames.ora
cp %_sourcedir/login.sql* %i/etc/login.sql
