### RPM cms prodagent PRODAGENT_0_0_17
## INITENV +PATH PYTHONPATH %i/lib

%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=PRODAGENT&export=PRODAGENT&&tag=-r%{cvstag}&output=/PRODAGENT.tar.gz
Requires: python mysql py2-mysqldb dbs dls boss

%prep
%setup -n PRODAGENT
%build
%install
make PREFIX=%i install
mkdir -p %i/bin
cp bin/* %{i}/bin
mkdir -p %{i}/etc/profile.d
mkdir -p %i/workdir

(echo "#!/bin/sh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.sh"; \
 echo "source $MYSQL_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_MYSQLDB_ROOT/etc/profile.d/init.sh"; \
 echo "source $DBS_ROOT/etc/profile.d/init.sh"; \
 echo "source $DLS_ROOT/etc/profile.d/init.sh"; \
 echo "source $BOSS_ROOT/etc/profile.d/init.sh" ) > %{i}/etc/profile.d/dependencies-setup.sh

(echo "#!/bin/tcsh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.csh"; \
 echo "source $MYSQL_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_MYSQLDB_ROOT/etc/profile.d/init.csh"; \
 echo "source $DBS_ROOT/etc/profile.d/init.csh"; \
 echo "source $DLS_ROOT/etc/profile.d/init.csh"; \
 echo "source $BOSS_ROOT/etc/profile.d/init.csh" ) > %{i}/etc/profile.d/dependencies-setup.csh

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
