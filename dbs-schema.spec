### RPM cms dbs-schema v00_00_14

%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=DBS/Schema/NeXtGen&export=DBS/Schema/NeXtGen&tag=-r%{cvstag}&output=/dbs-schema.tar.gz
Requires: mysql oracle

%prep
%setup -n DBS
%build
(make DBSHOME=%_builddir/DBS/Schema/NeXtGen )

%install
ls -l Schema/NeXtGen
cp -r Schema/NeXtGen/* %{i}/

