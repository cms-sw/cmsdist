### RPM cms icc-scram 16.0beta
## INITENV SETV INTEL_LICENSE_FILE  /afs/cern.ch/sw/IntelSoftware/linux/x86_64/xe2016/licenses
## NOCOMPILER
Requires: icc-provides
%prep
%build
%install
cd %i
ln -s /afs/cern.ch/sw/IntelSoftware/linux/x86_64/xe2016/compilers_and_libraries_2016.0.056/linux installation
ln -s /afs/cern.ch/sw/IntelSoftware/linux/x86_64/xe2016/compilers_and_libraries_2016.0.056/linux ifort
