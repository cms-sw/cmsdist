### RPM external rocm 5.4.3
## NOCOMPILER

%if "%{rhel}" == "7"
# allow rpm2cpio dependency on the bootstrap bundle
%undefine drop_bootstrap_lib
%define drop_bootstrap_lib true
%define repository repo.radeon.com/rocm/yum
%else
%define repository repo.radeon.com/rocm/rhel%{rhel}
%endif

Source0: https://%{repository}/%{realversion}/main/comgr-2.4.0.50403-121.el%{rhel}.%{_arch}.rpm
Source1: https://%{repository}/%{realversion}/main/hip-devel-5.4.22804.50403-121.el%{rhel}.%{_arch}.rpm
Source2: https://%{repository}/%{realversion}/main/hip-runtime-amd-5.4.22804.50403-121.el%{rhel}.%{_arch}.rpm
Source3: https://%{repository}/%{realversion}/main/hsa-rocr-1.7.0.50403-121.el%{rhel}.%{_arch}.rpm
Source4: https://%{repository}/%{realversion}/main/rocm-core-5.4.3.50403-121.el%{rhel}.%{_arch}.rpm
Source5: https://%{repository}/%{realversion}/main/rocm-dbgapi-0.68.0.50403-121.el%{rhel}.%{_arch}.rpm
Source6: https://%{repository}/%{realversion}/main/rocm-device-libs-1.0.0.50403-121.el%{rhel}.%{_arch}.rpm
Source7: https://%{repository}/%{realversion}/main/rocm-llvm-15.0.0.23045.50403-121.el%{rhel}.%{_arch}.rpm
Source8: https://%{repository}/%{realversion}/main/rocm-smi-lib-5.0.0.50403-121.el%{rhel}.%{_arch}.rpm
Source9: https://%{repository}/%{realversion}/main/rocminfo-1.0.0.50403-121.el%{rhel}.%{_arch}.rpm
Requires: numactl
Requires: python3

%prep

%build
rpm2cpio %{SOURCE0} | cpio -idmv
rpm2cpio %{SOURCE1} | cpio -idmv
rpm2cpio %{SOURCE2} | cpio -idmv
rpm2cpio %{SOURCE3} | cpio -idmv
rpm2cpio %{SOURCE4} | cpio -idmv
rpm2cpio %{SOURCE5} | cpio -idmv
rpm2cpio %{SOURCE6} | cpio -idmv
rpm2cpio %{SOURCE7} | cpio -idmv
rpm2cpio %{SOURCE8} | cpio -idmv
rpm2cpio %{SOURCE9} | cpio -idmv

%install
rmdir %{i}
mv opt/rocm-%{realversion} %{i}
rm -rf opt
rm -rf usr

# hip-devel postinstall
ln -s -f amd_detail    %{i}/include/hip/hcc_detail
ln -s -f nvidia_detail %{i}/include/hip/nvcc_detail
ln -s -f amd_detail    %{i}/hip/include/hip/hcc_detail
ln -s -f nvidia_detail %{i}/hip/include/hip/nvcc_detail

# hip-runtime-amd postinstall
mkdir -p %{i}/hip/lib/cmake/hip
mkdir -p %{i}/hip/lib/cmake/hip-lang
ln -r -s -f %{i}/lib/cmake/hip/hip-targets*           %{i}/hip/lib/cmake/hip/
ln -r -s -f %{i}/lib/cmake/hip-lang/hip-lang-targets* %{i}/hip/lib/cmake/hip-lang/

# rocm-llvm postinstall
mkdir -p %{i}/bin
ln -r -s -f %{i}/llvm/bin/amdclang     %{i}/bin/
ln -r -s -f %{i}/llvm/bin/amdclang++   %{i}/bin/
ln -r -s -f %{i}/llvm/bin/amdclang-cl  %{i}/bin/
ln -r -s -f %{i}/llvm/bin/amdclang-cpp %{i}/bin/
ln -r -s -f %{i}/llvm/bin/amdflang     %{i}/bin/
ln -r -s -f %{i}/llvm/bin/amdlld       %{i}/bin/

# replace '/usr/libexec/platform-python' with '/usr/bin/env python3'
find %{i}/bin/ %{i}/libexec/ %{i}/llvm/bin/ %{i}/llvm/lib/ -type f | xargs -r \
  grep '#! */usr/libexec/platform-python' -l | xargs -r \
  sed -e'1 s|#! */usr/libexec/platform-python|#!/usr/bin/env python3|' -s -i

%post
