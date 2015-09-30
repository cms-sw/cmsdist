### RPM cms icc-scram 2016.0.109
## INITENV SETV INTEL_LICENSE_FILE  /afs/cern.ch/sw/IntelSoftware/linux/x86_64/xe2016/licenses
## NOCOMPILER
Requires: icc-provides
%prep
%build
%install
cd %i
ln -s /afs/cern.ch/sw/IntelSoftware/linux/x86_64/xe2016/compilers_and_libraries_%{realversion}/linux installation
ln -s /afs/cern.ch/sw/IntelSoftware/linux/x86_64/xe2016/compilers_and_libraries_%{realversion}/linux ifort
