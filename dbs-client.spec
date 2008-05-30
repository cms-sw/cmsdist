### RPM cms dbs-client DBS_1_1_6_pre2
## INITENV +PATH PYTHONPATH %i/lib/

%define cvstag %{realversion}
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
Source: %cvsserver&strategy=checkout&module=DBS/Clients/Python&nocache=true&export=DBS&tag=-r%{cvstag}&output=/dbs-client.tar.gz
Requires: python openssl py2-zsi


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
 echo "source $PY2_ZSI_ROOT/etc/profile.d/init.sh"; \
 ) > %{i}/etc/profile.d/dependencies-setup.sh

(echo "#!/bin/tcsh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.csh"; \
 echo "source $OPENSSL_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_ZSI_ROOT/etc/profile.d/init.csh"; \
 ) > %{i}/etc/profile.d/dependencies-setup.csh

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=dbs-client version=%v>
<client>
 <Environment name=DBS_CLIENT_BASE default="%i"></Environment>
</client>
<Runtime name=PATH value="$DBS_CLIENT_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
%{relocateConfig}etc/scram.d/%n
