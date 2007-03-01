### RPM cms dbs-schema v00_00_12
## INITENV +PATH PYTHONPATH %i/lib

%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=DBS/Schema/NeXtGen&export=DBS/Schema/NeXtGen&tag=-r%{cvstag}&output=/dbs-schema.tar.gz
Requires: python

%prep
%setup -n DBS
%build
(make DBSHOME=%_builddir/DBS/Schema/NeXtGen )

%install
mkdir -p %i/bin
mkdir -p %i/lib/
ls -l Schema/NeXtGen
cp -r Schema/NeXtGen/* %i/lib/

