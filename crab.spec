### RPM cms crab CRAB_2_1_0_pre1
## INITENV +PATH PYTHONPATH %i/python
## INITENV +PATH PYTHONPATH %i/PsetCode
## INITENV +PATH PATH %i/python
## INITENV SET CRABPYTHON %i/python
## INITENV SET CRABDIR %i
## INITENV SET CRABSCRIPT %i/script
#
%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=CRAB&export=CRAB&&tag=-r%{cvstag}&output=/CRAB.tar.gz
Requires: python dbs-client dls-client prodcommon sqlite py2-pysqlite
Provides: libgridsite.so.1.1
%prep
%setup -n CRAB
%build
%install
rm -r script/dbDirectUpdatorMySQL
rm -rf %i
mkdir -p %i
cp -r ./* %i
mkdir -p %{i}/etc/profile.d

(echo "#!/bin/sh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.sh"; \
 echo "source $DBS_CLIENT_ROOT/etc/profile.d/init.sh"; \
 echo "source $DLS_CLIENT_ROOT/etc/profile.d/init.sh"; \
 echo "source $PRODCOMMON_ROOT/etc/profile.d/init.sh"; \
 echo "source $SQLITE_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_PYSQLITE_ROOT/etc/profile.d/init.sh"; ) > %{i}/etc/profile.d/dependencies-setup.sh

(echo "#!/bin/tcsh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.csh"; \
 echo "source $DBS_CLIENT_ROOT/etc/profile.d/init.csh"; \
 echo "source $DLS_CLIENT_ROOT/etc/profile.d/init.csh"; \
 echo "source $PRODCOMMON_ROOT/etc/profile.d/init.csh"; \
 echo "source $BOSS_ROOT/etc/profile.d/init.csh"; \
 echo "source $SQLITE_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_PYSQLITE_ROOT/etc/profile.d/init.csh"; ) > %{i}/etc/profile.d/dependencies-setup.csh

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh


