### RPM external icx 2022
## NOCOMPILER
Source: none
Provides: libimf.so()(64bit)
Provides: libintlc.so.5()(64bit)
Provides: libirng.so()(64bit)
Provides: libsvml.so()(64bit)

%prep
%build
%install
%post
ln -s /cvmfs/projects.cern.ch/intelsw/oneAPI/linux/x86_64/%{realversion}/compiler/latest/linux $RPM_INSTALL_PREFIX/%{pkgrel}/installation

