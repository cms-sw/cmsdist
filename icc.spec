### RPM external icc 2020.4.304
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
ln -s /cvmfs/projects.cern.ch/intelsw/psxe/linux/x86_64/2020/compilers_and_libraries_%{realversion}/linux $RPM_INSTALL_PREFIX/%{pkgrel}/installation

