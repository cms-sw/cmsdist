### RPM cms icc-scram 2017.0.064
## INITENV SETV INTEL_LICENSE_FILE /afs/cern.ch/sw/IntelSoftware/linux/x86_64/xe2017/beta_license/BETA____B92M-3G387F6M.LIC
## NOCOMPILER
Requires: icc-provides
%prep
%build
%install
cd %i
ln -s /afs/cern.ch/sw/IntelSoftware/linux/x86_64/xe2017/compilers_and_libraries_%{realversion}/linux installation
ln -s /afs/cern.ch/sw/IntelSoftware/linux/x86_64/xe2017/compilers_and_libraries_%{realversion}/linux ifort
