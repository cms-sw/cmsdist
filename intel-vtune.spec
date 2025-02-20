### RPM external intel-vtune 2025.0
## NOCOMPILER
## NO_AUTO_DEPENDENCY
## NO_VERSION_SUFFIX

%define year %(echo %realversion | cut -d. -f1)

## INITENV SET INTEL_VTUNE_INSTALLDIR /cvmfs/projects.cern.ch/intelsw/oneAPI/linux/x86_64/%{year}/vtune/%{realversion}

Source: none

%prep
%build
%install
