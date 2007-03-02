### RPM cms dbs-client v00_00_14
## INITENV +PATH PYTHONPATH %i/lib

%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=DBS/Clients/Python&export=DBS/Clients/Python&tag=-r%{cvstag}&output=/dbs-client.tar.gz
Requires: python

%prep
%setup -n DBS
%build
(make DBSHOME=%_builddir/DBS/Clients/Python )

%install
mkdir -p %{i}/bin
mkdir -p %{i}/lib
cp -r Clients/Python/* %{i}/lib/

