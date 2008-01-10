### RPM cms dbs-client DBS_1_0_9_pre3
## INITENV +PATH PYTHONPATH %i/lib/Clients/Python
#
#
%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=DBS/Clients/Python&export=DBS/Clients/Python&tag=-r%{cvstag}&output=/dbs-client.tar.gz
Requires: python openssl


%prep
%setup -n DBS
%build
(make DBSHOME=%_builddir/DBS/Clients/Python )

%install
mkdir -p %{i}/bin
mkdir -p %{i}/lib
mkdir -p %{i}/etc/profile.d
cp -r Clients/Python/* %{i}/lib/

(echo "#!/bin/sh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.sh"; \
 echo "source $OPENSSL_ROOT/etc/profile.d/init.sh"; \
 ) > %{i}/etc/profile.d/dependencies-setup.sh

(echo "#!/bin/tcsh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.csh"; \
 echo "source $OPENSSL_ROOT/etc/profile.d/init.csh"; \
 ) > %{i}/etc/profile.d/dependencies-setup.csh

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
