### RPM external rocm 6.2.4

# AMD repository with RPM packages for RHEL 8 and 9
%define repository repo.radeon.com/rocm/rhel%{rhel}

# AMD repositories are numbered 6.2, 6.2.1, 6.2.2, ..., 6.3
# without any .0 in the directory name
%define repoversion %(echo %{realversion} | sed -e's/\.0$//')

# ROCm branch, e.g. 5.6.x, 6.2.x
%define rocm_branch %(echo %{realversion} | cut -d. -f1-2).x

# git branch, tag and directory name for rocprofiler-register
%define rocprofiler_register_branch rocm-%{rocm_branch}
%define rocprofiler_register_tag    rocm-%{realversion}
%define rocprofiler_register_pkg    rocprofiler-register-%{rocprofiler_register_tag}

Source0: https://%{repository}/%{repoversion}/main/comgr-2.8.0.60204-139.el%{rhel}.%{_arch}.rpm
Source1: https://%{repository}/%{repoversion}/main/hipcc-1.1.1.60204-139.el%{rhel}.%{_arch}.rpm
Source2: https://%{repository}/%{repoversion}/main/hip-devel-6.2.41134.60204-139.el%{rhel}.%{_arch}.rpm
Source3: https://%{repository}/%{repoversion}/main/hip-runtime-amd-6.2.41134.60204-139.el%{rhel}.%{_arch}.rpm
Source4: https://%{repository}/%{repoversion}/main/hsa-rocr-1.14.0.60204-139.el%{rhel}.%{_arch}.rpm
Source5: https://%{repository}/%{repoversion}/main/rocm-core-6.2.4.60204-139.el%{rhel}.%{_arch}.rpm
Source6: https://%{repository}/%{repoversion}/main/rocm-dbgapi-0.76.0.60204-139.el%{rhel}.%{_arch}.rpm
Source7: https://%{repository}/%{repoversion}/main/rocm-device-libs-1.0.0.60204-139.el%{rhel}.%{_arch}.rpm
Source8: https://%{repository}/%{repoversion}/main/rocm-llvm-18.0.0.24392.60204-139.el%{rhel}.%{_arch}.rpm
Source9: https://%{repository}/%{repoversion}/main/rocm-smi-lib-7.3.0.60204-139.el%{rhel}.%{_arch}.rpm
Source10: https://%{repository}/%{repoversion}/main/rocminfo-1.0.0.60204-139.el%{rhel}.%{_arch}.rpm
Source11: https://%{repository}/%{repoversion}/main/openmp-extras-devel-18.62.0.60204-139.el%{rhel}.%{_arch}.rpm
Source12: https://%{repository}/%{repoversion}/main/openmp-extras-runtime-18.62.0.60204-139.el%{rhel}.%{_arch}.rpm
Source13: https://%{repository}/%{repoversion}/main/rocm-openmp-sdk-6.2.4.60204-139.el%{rhel}.%{_arch}.rpm
Source14: https://%{repository}/%{repoversion}/main/rocprim-devel-3.2.2.60204-139.el%{rhel}.%{_arch}.rpm
Source15: https://%{repository}/%{repoversion}/main/rocthrust-devel-3.1.1.60204-139.el%{rhel}.%{_arch}.rpm
Source16: https://%{repository}/%{repoversion}/main/rocprofiler-2.0.60204.60204-139.el%{rhel}.%{_arch}.rpm
Source17: https://%{repository}/%{repoversion}/main/rocprofiler-devel-2.0.60204.60204-139.el%{rhel}.%{_arch}.rpm
Source18: https://%{repository}/%{repoversion}/main/rocprofiler-docs-2.0.60204.60204-139.el%{rhel}.%{_arch}.rpm
Source19: https://%{repository}/%{repoversion}/main/rocprofiler-plugins-2.0.60204.60204-139.el%{rhel}.%{_arch}.rpm
Source20: https://%{repository}/%{repoversion}/main/amd-smi-lib-24.6.3.60204-139.el%{rhel}.%{_arch}.rpm

# sources for rocprofiler-register
Source21: git+https://github.com/ROCm/rocprofiler-register.git?obj=%{rocprofiler_register_branch}/%{rocprofiler_register_tag}&export=%{rocprofiler_register_pkg}&submodules=1&output=/%{rocprofiler_register_name}.tgz

BuildRequires: gmake cmake
Requires: numactl zstd
Requires: python3
AutoReq: no

%prep

# unpack rocprofiler-register
mkdir src
tar xavf %{SOURCE21} -C src

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

# build rocprofiler-register
mkdir -p build/rocprofiler-register
cd build/rocprofiler-register
cmake ../../src/%{rocprofiler_register_pkg} -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=%{i}
make all -j %{compiling_processes}

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

# instal rocprofiler-register
cd build/rocprofiler-register
make install

%post
