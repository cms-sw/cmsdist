### RPM cms prodagent 0.1
## INITENV +PATH PYTHONPATH %i/lib/python
%define cvstag pe20060403
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=MCPROTO&export=MCPROTO&&tag=-r%{cvstag}&output=/MCPROTO.tar.gz
Requires: python mysql py2-mysqldb dbs dls boss

%prep
%setup -n MCPROTO
%build
mkdir -p %i/lib/python
PYTHONPATH=%_builddir/MCPROTO/src/python:$PYTHONPATH
PRODAGENT_DIR=%i/lib/python ; export PRODAGENT_DIR
DBS_CLIENT_DIR=$DBS_ROOT; export DBS_CLIENT_DIR
DLS_CLIENT_DIR=$DLS_ROOT; export DLS_CLIENT_DIR

python install/configure.py 
%install
mkdir -p %i/lib/python
mkdir -p %i/share
cp -r ./src/python %i/lib
cp -r ./src/sql %i/share
