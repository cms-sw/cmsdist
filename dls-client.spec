### RPM cms dls-client DLS_1_0_3
## INITENV +PATH PATH %{i}/Server/SimpleServer
## INITENV +PATH PATH %{i}/Client/bin
## INITENV +PATH PYTHONPATH %{i}/Client/lib
%define cvstag %realversion
%define compProjectName DLS
%define srctree DLS
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=%{srctree}&export=%{compProjectName}&&tag=-r%{cvstag}&output=/DLS.tar.gz
Requires: python dbs-client 
%prep
%setup -n DLS
perl -p -i -e "s|#!/usr/bin/python|#!/usr/bin/env python|" $(find .)
%build
%install
rm -r Documentation
rm -r Import
rm -r Server
#
cd Client
make
rm -r lib/ZSI
rm -r lib/*PyXML*
rm lib/pyexpat*
mkdir -p %{i}/Client/bin
mv lib/dls-* %{i}/Client/bin/.
mv lib/dli-* %{i}/Client/bin/.
cp -r lib %{i}/Client/.

cd ..

mkdir -p %{i}/etc/profile.d
 
echo "test"
(echo "#!/bin/sh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.sh"; \
 echo "source $DBS_CLIENT_ROOT/etc/profile.d/init.sh"; 
) > %{i}/etc/profile.d/dependencies-setup.sh
                                                                                                     
(echo "#!/bin/tcsh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.csh"; \
 echo "source $DBS_CLIENT_ROOT/etc/profile.d/init.csh"; 
) > %{i}/etc/profile.d/dependencies-setup.csh
                                                                                                     
%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

