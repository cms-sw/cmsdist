### RPM cms prodagent PRODAGENT_0_0_3
## INITENV +PATH PYTHONPATH %i/lib
%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=PRODAGENT&export=PRODAGENT&&tag=-r%{cvstag}&output=/PRODAGENT.tar.gz
Requires: python mysql py2-mysqldb dbs dls boss

%prep
%setup -n PRODAGENT
%build
mkdir -p etc/profile.d
echo "!/bin/sh" > etc/profile.d/setup.sh
echo "source $PYTHON_ROOT/etc/profile.d/init.sh" >> etc/profile.d/dependencies-setup.sh
echo "source $MYSQL_ROOT/etc/profile.d/init.sh" >> etc/profile.d/dependencies-setup.sh
echo "source $PY2_MYSQLDB_ROOT/etc/profile.d/init.sh" >> etc/profile.d/dependencies-setup.sh
echo "source $DBS_ROOT/etc/profile.d/init.sh" >> etc/profile.d/dependencies-setup.sh
echo "source $DLS_ROOT/etc/profile.d/init.sh" >> etc/profile.d/dependencies-setup.sh
echo "source $BOSS_ROOT/etc/profile.d/init.sh" >> etc/profile.d/dependencies-setup.sh

%install
make PREFIX=%i install
mkdir -p %{i}/etc/profile.d

(echo "#!/bin/sh"; \
echo "source $PYTHON_ROOT/etc/profile.d/init.sh"; \
echo "source $MYSQL_ROOT/etc/profile.d/init.sh"; \
echo "source $PY2_MYSQLDB_ROOT/etc/profile.d/init.sh"; \
echo "source $DBS_ROOT/etc/profile.d/init.sh"; \
echo "source $DLS_ROOT/etc/profile.d/init.sh"; \
echo "source $BOSS_ROOT/etc/profile.d/init.sh")  > %i/etc/profile.d/dependencies-setup.sh
%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
