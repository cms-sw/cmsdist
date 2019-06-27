### RPM cms icc-scram 2018.0.128
## NOCOMPILER
Requires: icc-provides
%prep
%build
%install
cd %i
ln -s /cvmfs/projects.cern.ch/intelsw/psxe/linux/x86_64/2018/compilers_and_libraries_%{realversion}/linux installation
ln -s /cvmfs/projects.cern.ch/intelsw/psxe/linux/x86_64/2018/compilers_and_libraries_%{realversion}/linux ifort
# bla bla
