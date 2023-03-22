### RPM external rocm-rocrand 5.4.3
## NOCOMPILER

%if "%{rhel}" == "7"
# allow rpm2cpio dependency on the bootstrap bundle
%undefine drop_bootstrap_lib
%define drop_bootstrap_lib true
%define repository repo.radeon.com/rocm/yum
%else
%define repository repo.radeon.com/rocm/rhel%{rhel}
%endif

Source0: https://%{repository}/%{realversion}/main/rocrand-2.10.9.50403-121.el%{rhel}.%{_arch}.rpm
Source1: https://%{repository}/%{realversion}/main/rocrand-devel-2.10.9.50403-121.el%{rhel}.%{_arch}.rpm
Requires: rocm

%prep

%build
rpm2cpio %{SOURCE0} | cpio -idmv
rpm2cpio %{SOURCE1} | cpio -idmv

%install
rmdir %{i}
mv opt/rocm-%{realversion} %{i}
rm -rf opt
rm -rf usr

%post
