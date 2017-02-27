### RPM cms icc-scram 2017.2.174
## NOCOMPILER
Requires: icc-provides
%prep
%build
%install
cd %i
ln -s /cvmfs/projects.cern.ch/intelsw/psxe/linux/x86_64/2017/compilers_and_libraries_%{realversion}/linux installation
ln -s /cvmfs/projects.cern.ch/intelsw/psxe/linux/x86_64/2017/compilers_and_libraries_%{realversion}/linux ifort
