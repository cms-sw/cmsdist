### RPM external zlib 1.0
#test 
%ifarch x86_64
Requires: zlib-x86_64
%define ZLIB_PKG ZLIB_X86_64
%else
Requires: zlib-non-x86_64
%define ZLIB_PKG ZLIB_NON_X86_64
%endif

%prep
%build
%install
%post
cp ${RPM_INSTALL_PREFIX}/%{cmsplatf}/$(echo %{directpkgreqs} | tr ' ' '\n' | grep /zlib-)/etc/profile.d/init.* ${RPM_INSTALL_PREFIX}/%{pkgrel}/etc/profile.d
sed -i -e 's|%{ZLIB_PKG}_|ZLIB_|' ${RPM_INSTALL_PREFIX}/%{pkgrel}/etc/profile.d/init.*

