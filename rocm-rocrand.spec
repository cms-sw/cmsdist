### RPM external rocm-rocrand 5.6.0
## NOCOMPILER

%if "%{rhel}" == "7"
# allow rpm2cpio dependency on the bootstrap bundle
%undefine drop_bootstrap_lib
%define drop_bootstrap_lib true
%define repository repo.radeon.com/rocm/yum
%else
%define repository repo.radeon.com/rocm/rhel%{rhel}
%endif

# AMD repositories are numbered 5.5, 5.5.1, 5.5.2, ..., 5.6
# without any .0 in the directory name
%define repoversion %(echo %{realversion} | sed -e's/\.0$//')

Source0: https://%{repository}/%{repoversion}/main/rocrand-2.10.17.50600-67.el%{rhel}.%{_arch}.rpm
Source1: https://%{repository}/%{repoversion}/main/rocrand-devel-2.10.17.50600-67.el%{rhel}.%{_arch}.rpm
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
