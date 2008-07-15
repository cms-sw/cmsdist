### RPM cms prodagent PRODAGENT_0_0_13
## INITENV +PATH PYTHONPATH %i/lib
#
#
%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=PRODAGENT&export=PRODAGENT&&tag=-r%{cvstag}&output=/PRODAGENT.tar.gz
#Requires: webtools python mysql py2-mysqldb dbs-client boss prodcommon openssl cherrypy PHEDEX-micro
Requires: webtools mysql py2-mysqldb dbs-client boss prodcommon py2-pyxml PHEDEX-micro

%prep
%setup -n PRODAGENT
%build
%install
make PREFIX=%i install
mkdir -p %i/bin
cp bin/prod* %{i}/bin
mkdir -p %i/test
cp -R test/* %i/test/
mkdir -p %i/util
cp -R util/* %i/util/
mkdir -p %{i}/etc/profile.d
mkdir -p %i/workdir

(echo "#!/bin/sh"; \
# echo "source $PYTHON_ROOT/etc/profile.d/init.sh"; \
# echo "source $OPENSSL_ROOT/etc/profile.d/init.sh"; \
 echo "source $MYSQL_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_MYSQLDB_ROOT/etc/profile.d/init.sh"; \
 echo "source $DBS_CLIENT_ROOT/etc/profile.d/init.sh"; \
 echo "source $PRODCOMMON_ROOT/etc/profile.d/init.sh"; \
# echo "source $CHERRYPY_ROOT/etc/profile.d/init.sh"; \
 echo "source $PHEDEX_MICRO_ROOT/etc/profile.d/init.sh"; \
 echo "source $WEBTOOLS_ROOT/etc/profile.d/init.sh"; \
 echo "source $BOSS_ROOT/etc/profile.d/init.sh" ) > %{i}/etc/profile.d/dependencies-setup.sh

(echo "#!/bin/tcsh"; \
# echo "source $PYTHON_ROOT/etc/profile.d/init.csh"; \
# echo "source $OPENSSL_ROOT/etc/profile.d/init.csh"; \
 echo "source $MYSQL_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_MYSQLDB_ROOT/etc/profile.d/init.csh"; \
 echo "source $DBS_CLIENT_ROOT/etc/profile.d/init.csh"; \
 echo "source $PRODCOMMON_ROOT/etc/profile.d/init.csh"; \
# echo "source $CHERRYPY_ROOT/etc/profile.d/init.csh"; \
 echo "source $PHEDEX_MICRO_ROOT/etc/profile.d/init.csh"; \
 echo "source $WEBTOOLS_ROOT/etc/profile.d/init.csh"; \
 echo "source $BOSS_ROOT/etc/profile.d/init.csh" ) > %{i}/etc/profile.d/dependencies-setup.csh


%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

