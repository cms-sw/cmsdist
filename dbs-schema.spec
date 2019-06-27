### RPM cms dbs-schema DBS_2_1_5

%define cvstag %{realversion}
#Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=DBS/Schema/NeXtGen&export=DBS/Schema/NeXtGen&tag=-r%{cvstag}&output=/dbs-schema.tar.gz
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
Source: %cvsserver&strategy=checkout&module=DBS/Schema/NeXtGen&nocache=true&export=DBS&tag=-r%{cvstag}&output=/dbs-schema.tar.gz
Requires: mysql oracle

%prep
%setup -n DBS
%build
(make DBSHOME=%_builddir/DBS/Schema/NeXtGen )

%install
mkdir -p %{i}/etc/profile.d
mkdir -p %{i}/lib/Schema/NeXtGen
cp -r Schema/NeXtGen/* %{i}/lib/Schema/NeXtGen/

(echo "#!/bin/sh"; \
 echo "source $ORACLE_ROOT/etc/profile.d/init.sh"; \
 echo "source $MYSQL_ROOT/etc/profile.d/init.sh"; \
 ) > %{i}/etc/profile.d/dependencies-setup.sh

(echo "#!/bin/tcsh"; \
 echo "source $ORACLE_ROOT/etc/profile.d/init.csh"; \
 echo "source $MYSQL_ROOT/etc/profile.d/init.csh"; \
 ) > %{i}/etc/profile.d/dependencies-setup.csh

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=dbs-schema version=%v>
<client>
 <Environment name=DBS_SCHEMA_BASE default="%i"></Environment>
</client>
<Runtime name=PATH value="$DBS_SCHEMA_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
%{relocateConfig}etc/scram.d/%n
# bla bla
