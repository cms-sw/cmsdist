### RPM cms prodagent PRODAGENT_0_0_0
## INITENV +PATH PYTHONPATH %i/lib
%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=PRODAGENT&export=PRODAGENT&&tag=-r%{cvstag}&output=/PRODAGENT.tar.gz
Requires: python mysql py2-mysqldb dbs dls boss

%prep
%setup -n PRODAGENT
%build
make

%install
cp -r bin %{i}
cp -r lib %{i}
