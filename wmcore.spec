### RPM cms wmcore WMCORE_0_0_1
## INITENV +PATH PYTHONPATH %i/lib

%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=WMCORE&export=WMCORE&&tag=-r%{cvstag}&output=/WMCORE.tar.gz
Requires: python py2-sqlalchemy

%prep
%setup -n WMCORE
%build
%install
make PREFIX=%i install
mkdir -p %i
cp -r * %i

mkdir -p %{i}/etc/profile.d
mkdir -p %i/workdir

(echo "#!/bin/sh"; \
 echo "source $PY2_SQLALCHEMY_ROOT/etc/profile.d/init.sh") > %{i}/etc/profile.d/dependencies-setup.sh

(echo "#!/bin/tcsh"; \
 echo "source $PY2_SQLALCHEMY_ROOT/etc/profile.d/init.csh") > %{i}/etc/profile.d/dependencies-setup.csh


%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

