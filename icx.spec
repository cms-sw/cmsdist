### RPM external icx 2023.2.0
## NOCOMPILER

%define year %(echo %realversion | cut -d. -f1)

Source: none
Provides: libimf.so()(64bit)
Provides: libintlc.so.5()(64bit)
Provides: libirng.so()(64bit)
Provides: libsvml.so()(64bit)

%prep
%build
%install
%post
ln -s /cvmfs/projects.cern.ch/intelsw/oneAPI/linux/x86_64/%{year}/compiler/%{realversion}/linux $RPM_INSTALL_PREFIX/%{pkgrel}/installation
