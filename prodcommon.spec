### RPM cms prodcommon PRODCOMMON_0_2_0
Requires: gcc-wrapper
## INITENV +PATH PYTHONPATH %i/lib

%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=PRODCOMMON&export=PRODCOMMON&&tag=-r%{cvstag}&output=/PRODCOMMON.tar.gz
Requires: python
%prep
%setup -n PRODCOMMON
%build
## IMPORT gcc-wrapper
%install
make PREFIX=%i install
mkdir -p %i
cp -r * %i
