### RPM cms prodagent PRODAGENT_0_12_13_patch5
## INITENV +PATH PYTHONPATH %i/lib
## INITENV +PATH PYTHONPATH $WEBTOOLS_ROOT/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/Tools/GraphTool/src
## INITENV +PATH PYTHONPATH $PY2_PIL_ROOT/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/PIL
#
#The first line of this file you only edit the version name. This name
# is equal to the with which you tagged the release in cvs. Note: if you 
# do not change the tag and already have uploaded the build packages
# nothing will be created as the cms build application checks the repository.

%define cvstag %v
# where the package is located. Normally this does not change
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=PRODAGENT&export=PRODAGENT&&tag=-r%{cvstag}&output=/PRODAGENT.tar.gz
# dependencies. THis can change from time to time. The names correspond with the spec files of the saem name.
Requires: webtools mysql py2-mysqldb dbs-client prodcommon py2-pyxml PHEDEX-micro py2-numpy py2-matplotlib py2-pil py2-pyopenssl wmcore dls-client boss

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

#When you add a new packages you also add its root to the list below
# for sh and csh. This ensures that all the settings are set correctly
# when the init file of the package is sourced.

(echo "#!/bin/sh"; \
 echo "source $MYSQL_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_MYSQLDB_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_PYXML_ROOT/etc/profile.d/init.sh"; \
 echo "source $DBS_CLIENT_ROOT/etc/profile.d/init.sh"; \
 echo "source $DLS_CLIENT_ROOT/etc/profile.d/init.sh"; \
 echo "source $PRODCOMMON_ROOT/etc/profile.d/init.sh"; \
 echo "source $BOSS_ROOT/etc/profile.d/init.sh"; \
 echo "source $PHEDEX_MICRO_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_NUMPY_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_MATPLOTLIB_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_PIL_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_PYOPENSSL_ROOT/etc/profile.d/init.sh"; \
 echo "source $WEBTOOLS_ROOT/etc/profile.d/init.sh"; \
 echo "source $WMCORE_ROOT/etc/profile.d/init.sh" ) > %{i}/etc/profile.d/dependencies-setup.sh

(echo "#!/bin/tcsh"; \
 echo "source $MYSQL_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_MYSQLDB_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_PYXML_ROOT/etc/profile.d/init.csh"; \
 echo "source $DBS_CLIENT_ROOT/etc/profile.d/init.csh"; \
 echo "source $DLS_CLIENT_ROOT/etc/profile.d/init.csh"; \
 echo "source $PRODCOMMON_ROOT/etc/profile.d/init.csh"; \
 echo "source $BOSS_ROOT/etc/profile.d/init.csh"; \
 echo "source $PHEDEX_MICRO_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_NUMPY_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_MATPLOTLIB_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_PIL_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_PYOPENSSL_ROOT/etc/profile.d/init.csh"; \
 echo "source $WEBTOOLS_ROOT/etc/profile.d/init.csh"; \
 echo "source $WMCORE_ROOT/etc/profile.d/init.csh" ) > %{i}/etc/profile.d/dependencies-setup.csh


%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

