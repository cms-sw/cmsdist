### RPM external opencl 1.1
## NOCOMPILER
%define skip_license_checks 1

%prep
# NOP

%build
# NOP

%install
# NOP

%post
ln -s /usr/lib64/nvidia ${RPM_INSTALL_PREFIX}/%{pkgrel}/lib64
ln -s /usr/local/cuda/include ${RPM_INSTALL_PREFIX}/%{pkgrel}/include
