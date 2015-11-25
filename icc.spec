### RPM external icc composer_xe_2013.2.146
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
ln -s /afs/cern.ch/sw/IntelSoftware/linux/x86_64/xe2013/%{realversion} $RPM_INSTALL_PREFIX/%{pkgrel}/installation
