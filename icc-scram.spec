### RPM cms icc-scram 15.0.1
## NOCOMPILER
Requires: icc-provides
%prep
%build
%install
cd %i
ln -s /afs/cern.ch/sw/IntelSoftware/linux/x86_64/xe2015/composer_xe_2015.1.133 installation
ln -s /afs/cern.ch/sw/IntelSoftware/linux/x86_64/xe2015/composer_xe_2015.1.133 ifort
