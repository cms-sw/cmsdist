### RPM cms oracle-env 25.0
## NOCOMPILER
## INITENV +PATH SQLPATH %i/etc
## INITENV SET TNS_ADMIN %i/etc

Source0: http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/*checkout*/COMP/PHEDEX/Schema/login.sql?rev=1.2&cvsroot=CMSSW
Source1: http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/*checkout*/COMP/PHEDEX/Schema/tnsnames.ora?rev=1.35&cvsroot=CMSSW
%prep
%build
%install
mkdir -p %i/etc
# Create sqlnet.ora to quash ~/oradiag_$USER directories with oracle 11,
# as suggested by Andreas Valassi
cat << \EOF_SQLNET >%i/etc/sqlnet.ora
sqlnet.expire_time = 15
bequeath_detach = yes
DIAG_ADR_ENABLED = FALSE
DIAG_DDE_ENABLED = FALSE
EOF_SQLNET
cp %_sourcedir/tnsnames.ora* %i/etc/tnsnames.ora
cp %_sourcedir/login.sql* %i/etc/login.sql

%post
echo "ORACLE_ENV_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "set ORACLE_ENV_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh
