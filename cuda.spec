### RPM external cuda 1.0
## NOCOMPILER
%prep
%build
%install
%post
ln -s /usr/local/cuda $RPM_INSTALL_PREFIX/%{pkgrel}/installation
