### RPM cms icc-scram 15.0.0
%define icc    /oplashare/sw/linux/x86_64/intel/icc15beta2
%define ifort  /afs/cern.ch/sw/IntelSoftware/linux/x86_64/ifort15beta
## NOCOMPILER
%prep
%build
%install
cd %i
ln -s %{icc}   icc
ln -s %{ifort} ifort
