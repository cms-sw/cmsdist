### RPM external icc 2016.1.150
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
ln -s /afs/cern.ch/sw/IntelSoftware/linux/x86_64/xe2016/compilers_and_libraries_%{realversion}/linux $RPM_INSTALL_PREFIX/%{pkgrel}/installation
ln -s /afs/cern.ch/sw/IntelSoftware/linux/x86_64/xe2016/compilers_and_libraries_%{realversion}/linux $RPM_INSTALL_PREFIX/%{pkgrel}/ifort
