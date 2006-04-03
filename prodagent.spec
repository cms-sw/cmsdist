### RPM cms prodagent 0.1
## INITENV +PATH PYTHONPATH %i/lib/python
%define cvstag pe20060403
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=MCPROTO&export=MCPROTO&&tag=-r%{cvstag}&output=/MCPROTO.tar.gz
Requires: python

%prep
%setup -n MCPROTO
%build
%install
mkdir -p %i/lib/python
mkdir -p %i/share
cp -r ./src/python %i/lib
cp -r ./src/sql %i/share
