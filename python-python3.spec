### RPM external python-python3 1.0
## NOCOMPILER
Source: none
Requires: python3

%prep
%build
%install
%post
mkdir $RPM_INSTALL_PREFIX/%{pkgrel}/bin
ln -s ../../../../%{directpkgreqs}/bin/python3 $RPM_INSTALL_PREFIX/%{pkgrel}/bin/python
