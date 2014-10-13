### RPM cms icc-scram 15.0.0
## NOCOMPILER
Requires: icc-provides
%prep
%build
%install
cd %i
ln -s /afs/cern.ch/sw/IntelSoftware/linux/x86_64/xe2015/composer_xe_2015.0.090 installation
ln -s /afs/cern.ch/sw/IntelSoftware/linux/x86_64/xe2015/composer_xe_2015.0.090 ifort
