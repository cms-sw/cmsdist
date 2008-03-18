### RPM cms dls-client DLS_1_1_0_pre1
## INITENV +PATH PATH %{i}/Client/bin
## INITENV +PATH PYTHONPATH %{i}/Client/lib
%define cvstag %realversion
%define compProjectName DLS
%define srctree DLS/Client
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=%{srctree}&export=%{compProjectName}&&tag=-r%{cvstag}&output=/DLS.tar.gz
Requires: python dbs-client py2-pyxml
%prep
%setup -n DLS
perl -p -i -e "s|#!/usr/bin/python|#!/usr/bin/env python|" $(find .)
%build
%install
#
cd Client
make
mkdir -p %{i}/Client
cp -r lib %{i}/Client/.
cp -r bin %{i}/Client/.
#cp -r etc %{i}/Client/.

mkdir -p %{i}/etc/profile.d
 
echo "test"
(echo "#!/bin/sh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_PYXML_ROOT/etc/profile.d/init.sh"; \
 echo "source $DBS_CLIENT_ROOT/etc/profile.d/init.sh"; 
 echo "export DBS_CLIENT_CONFIG=$DBS_CLIENT_ROOT/lib/Clients/Python/DBSAPI/dbs.config"; 
) > %{i}/etc/profile.d/dependencies-setup.sh
                                                                                                     
(echo "#!/bin/tcsh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_PYXML_ROOT/etc/profile.d/init.csh"; \
 echo "source $DBS_CLIENT_ROOT/etc/profile.d/init.csh"; 
 echo "setenv DBS_CLIENT_CONFIG $DBS_CLIENT_ROOT/lib/Clients/Python/DBSAPI/dbs.config"; 
) > %{i}/etc/profile.d/dependencies-setup.csh
                                                                                                     
%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

