### RPM external rocm 5.6.1

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

Source0: https://%{repository}/%{repoversion}/main/comgr-2.5.0.50601-93.el%{rhel}.%{_arch}.rpm
Source1: https://%{repository}/%{repoversion}/main/hipcc-1.0.0.50601-93.el%{rhel}.%{_arch}.rpm
Source2: https://%{repository}/%{repoversion}/main/hip-devel-5.6.31062.50601-93.el%{rhel}.%{_arch}.rpm
Source3: https://%{repository}/%{repoversion}/main/hip-runtime-amd-5.6.31062.50601-93.el%{rhel}.%{_arch}.rpm
Source4: https://%{repository}/%{repoversion}/main/hsa-rocr-1.9.0.50601-93.el%{rhel}.%{_arch}.rpm
Source5: https://%{repository}/%{repoversion}/main/rocm-core-5.6.1.50601-93.el%{rhel}.%{_arch}.rpm
Source6: https://%{repository}/%{repoversion}/main/rocm-dbgapi-0.70.1.50601-93.el%{rhel}.%{_arch}.rpm
Source7: https://%{repository}/%{repoversion}/main/rocm-device-libs-1.0.0.50601-93.el%{rhel}.%{_arch}.rpm
Source8: https://%{repository}/%{repoversion}/main/rocm-llvm-16.0.0.23332.50601-93.el%{rhel}.%{_arch}.rpm
Source9: https://%{repository}/%{repoversion}/main/rocm-smi-lib-5.0.0.50601-93.el%{rhel}.%{_arch}.rpm
Source10: https://%{repository}/%{repoversion}/main/rocminfo-1.0.0.50601-93.el%{rhel}.%{_arch}.rpm
Source11: https://%{repository}/%{repoversion}/main/openmp-extras-devel-16.56.0.50601-93.el%{rhel}.%{_arch}.rpm
Source12: https://%{repository}/%{repoversion}/main/openmp-extras-runtime-16.56.0.50601-93.el%{rhel}.%{_arch}.rpm
Source13: https://%{repository}/%{repoversion}/main/rocm-openmp-sdk-5.6.1.50601-93.el%{rhel}.%{_arch}.rpm
Source14: https://%{repository}/%{repoversion}/main/rocprim-devel-2.13.0.50601-93.el%{rhel}.%{_arch}.rpm
Source15: https://%{repository}/%{repoversion}/main/rocthrust-devel-2.18.0.50601-93.el%{rhel}.%{_arch}.rpm
Source16: https://%{repository}/%{repoversion}/main/rocprofiler-2.0.0.50601-93.el%{rhel}.%{_arch}.rpm
Source17: https://%{repository}/%{repoversion}/main/rocprofiler-devel-2.0.0.50601-93.el%{rhel}.%{_arch}.rpm
Source18: https://%{repository}/%{repoversion}/main/rocprofiler-docs-2.0.0.50601-93.el%{rhel}.%{_arch}.rpm
Source19: https://%{repository}/%{repoversion}/main/rocprofiler-plugins-2.0.0.50601-93.el%{rhel}.%{_arch}.rpm
Source20: https://%{repository}/%{repoversion}/main/rocprofiler-samples-2.0.0.50601-93.el%{rhel}.%{_arch}.rpm
Source21: https://%{repository}/%{repoversion}/main/amd-smi-lib-1.0.0.50601-93.el%{rhel}.%{_arch}.rpm

Requires: numactl zstd
Requires: python3
AutoReq: no

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
rpm2cpio %{SOURCE10} | cpio -idmv
rpm2cpio %{SOURCE11} | cpio -idmv
rpm2cpio %{SOURCE12} | cpio -idmv
rpm2cpio %{SOURCE13} | cpio -idmv
rpm2cpio %{SOURCE14} | cpio -idmv
rpm2cpio %{SOURCE15} | cpio -idmv
rpm2cpio %{SOURCE16} | cpio -idmv
rpm2cpio %{SOURCE17} | cpio -idmv
rpm2cpio %{SOURCE18} | cpio -idmv
rpm2cpio %{SOURCE19} | cpio -idmv
rpm2cpio %{SOURCE20} | cpio -idmv
rpm2cpio %{SOURCE21} | cpio -idmv

%install
rmdir %{i}
mv opt/rocm-%{realversion} %{i}
rm -rf opt
rm -rf usr

# the hip directory is deprecated in favour of the main directory
rm -r -f %{i}/hip/

# hip-devel postinstall
ln -s -f amd_detail    %{i}/include/hip/hcc_detail
ln -s -f nvidia_detail %{i}/include/hip/nvcc_detail
# deprecated
#ln -s -f amd_detail    %{i}/hip/include/hip/hcc_detail
#ln -s -f nvidia_detail %{i}/hip/include/hip/nvcc_detail

# hip-runtime-amd postinstall
# deprecated
#mkdir -p %{i}/hip/lib/cmake/hip
#mkdir -p %{i}/hip/lib/cmake/hip-lang
#ln -r -s -f %{i}/lib/cmake/hip/hip-targets*           %{i}/hip/lib/cmake/hip/
#ln -r -s -f %{i}/lib/cmake/hip-lang/hip-lang-targets* %{i}/hip/lib/cmake/hip-lang/

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
