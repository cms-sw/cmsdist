### RPM external rocm-rocrand 6.2.4
## NOCOMPILER

%if 0%{?rhel} == 7
# allow rpm2cpio dependency on the bootstrap bundle
%undefine drop_bootstrap_lib
%define drop_bootstrap_lib true
%define repository repo.radeon.com/rocm/yum
%else
%define repository repo.radeon.com/rocm/rhel%{rhel}
%endif

# AMD repositories are numbered 6.1, 6.1.1, 6.1.2, ..., 6.2
# without any .0 in the directory name
%define repoversion %(echo %{realversion} | sed -e's/\.0$//')

Source0: https://%{repository}/%{repoversion}/main/rocrand-3.1.1.60204-139.el%{rhel}.%{_arch}.rpm
Source1: https://%{repository}/%{repoversion}/main/rocrand-devel-3.1.1.60204-139.el%{rhel}.%{_arch}.rpm
Requires: rocm
AutoReq: no

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
