### RPM cms prodagent PRODAGENT_0_0_0
## INITENV +PATH PYTHONPATH %i/lib/python
%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=PRODAGENT&export=PRODAGENT&&tag=-r%{cvstag}&output=/PRODAGENT.tar.gz
Requires: python mysql py2-mysqldb dbs dls boss

%prep
%setup -n PRODAGENT
%build
make
PYTHONPATH=%_builddir/PRODAGENT/src/python:$PYTHONPATH
PRODAGENT_DIR=%i/lib/python ; export PRODAGENT_DIR
DBS_CLIENT_DIR=$DBS_ROOT; export DBS_CLIENT_DIR
DLS_CLIENT_DIR=$DLS_ROOT; export DLS_CLIENT_DIR

python install/configure.py 
%install
> cp -r bin %{i}
> cp -r lib %{i}
