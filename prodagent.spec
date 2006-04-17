### RPM cms prodagent PRODAGENT_0_0_1
## INITENV +PATH PYTHONPATH %i/lib
## INITENV CMD source %i/etc/profile.d/dependencies-setup.sh
%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=PRODAGENT&export=PRODAGENT&&tag=-r%{cvstag}&output=/PRODAGENT.tar.gz
Requires: python mysql py2-mysqldb dbs dls boss

%prep
%setup -n PRODAGENT
%build
make
# 
mkdir -p etc/profile.d
echo "!/bin/sh" > etc/profile.d/setup.sh
echo "source $PYTHON_ROOT/etc/profile.d/init.sh" >> etc/profile.d/dependencies-setup.sh
echo "source $MYSQL_ROOT/etc/profile.d/init.sh" >> etc/profile.d/dependencies-setup.sh
echo "source $PY2_MYSQLDB_ROOT/etc/profile.d/init.sh" >> etc/profile.d/dependencies-setup.sh
echo "source $DBS_ROOT/etc/profile.d/init.sh" >> etc/profile.d/dependencies-setup.sh
echo "source $DLS_ROOT/etc/profile.d/init.sh" >> etc/profile.d/dependencies-setup.sh
echo "source $BOSS_ROOT/etc/profile.d/init.sh" >> etc/profile.d/dependencies-setup.sh

%install
mkdir -p %{i}/etc/profile.d
cp etc/profile.d/dependencies-setup.sh %{i}/etc/profile.d
cp -r bin %{i}
cp -r lib %{i}
%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
