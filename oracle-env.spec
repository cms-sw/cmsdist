### RPM cms oracle-env 29
## NOCOMPILER
## INITENV +PATH SQLPATH %i/etc
## INITENV SET TNS_ADMIN %i/etc

Source0: https://davidlt.web.cern.ch/davidlt/vault/oracle-env/29/login.sql
Source1: https://davidlt.web.cern.ch/davidlt/vault/oracle-env/29/tnsnames.ora
Source2: https://davidlt.web.cern.ch/davidlt/vault/oracle-env/29/sqlnet.ora
Patch0: oracle-env-online
%prep
%build
%install
mkdir -p %i/etc
cp %_sourcedir/sqlnet.ora %i/etc/sqlnet.ora
cp %_sourcedir/tnsnames.ora %i/etc/tnsnames.ora
cp %_sourcedir/login.sql %i/etc/login.sql
cd %i/etc
patch -p0 <%_sourcedir/oracle-env-online
