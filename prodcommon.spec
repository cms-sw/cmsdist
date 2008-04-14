### RPM cms prodcommon PRODCOMMON_0_9_0_pre1testCS3
## INITENV +PATH PYTHONPATH %i/lib

%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=PRODCOMMON&export=PRODCOMMON&&tag=-r%{cvstag}&output=/PRODCOMMON.tar.gz
Requires: python
%prep
%setup -n PRODCOMMON
%build
%install
make PREFIX=%i install
mkdir -p %i
cp -r * %i
