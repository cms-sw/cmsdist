### RPM cms dbs-libs DBS_2_0_3_pre2
## INITENV +PATH PYTHONPATH %i/lib/

%define cvstag %{realversion}
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
Source: %cvsserver&strategy=checkout&module=DBS/LibValut&nocache=true&export=DBS&tag=-r%{cvstag}&output=/dbs-libs.tar.gz

%prep
%setup -n DBS
%build
(make DBSHOME=%_builddir/DBS/LibValut )

%install
mkdir -p %{i}/bin
mkdir -p %{i}/lib
mkdir -p %{i}/etc/profile.d
cp -r LibValut/* %{i}/lib/

(echo "#!/bin/sh"; \
 ) > %{i}/etc/profile.d/dependencies-setup.sh

(echo "#!/bin/tcsh"; \
 ) > %{i}/etc/profile.d/dependencies-setup.csh

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=dbs-client version=%v>
<client>
 <Environment name=DBS_LIBS_BASE default="%i"></Environment>
</client>
<Runtime name=PATH value="$DBS_LIBS_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
%{relocateConfig}etc/scram.d/%n
