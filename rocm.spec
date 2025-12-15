### RPM external rocm 7.1.0
## INCLUDE cpp-standard
## INITENV SET HIP_PATH %{i}

%define repository repo.radeon.com/rocm/rhel%{rhel}

%if 0%{?rhel} == 9
# See https://github.com/ROCm/ROCm/issues/5617
# EL9 packages are actually EL8 artefacts
%define rpm_arch el8.%{_arch}
%else
%define rpm_arch el%{rhel}.%{_arch}
%endif

# AMD repositories are numbered 6.2, 6.2.1, 6.2.2, ..., 6.3
# without any .0 in the directory name
%define repoversion %(echo %{realversion} | sed -e's/\.0$//')

# ROCm branch, e.g. 5.6, 6.2
%define rocm_branch %(echo %{realversion} | cut -d. -f1-2)

# git branch, tag and directory name for rocprofiler-register
%define rocprofiler_register_branch release/rocm-rel-%{rocm_branch}
%define rocprofiler_register_tag    rocm-%{realversion}
%define rocprofiler_register_pkg    rocprofiler-register-%{rocprofiler_register_tag}

Source0: https://%{repository}/%{repoversion}/main/amd-smi-lib-26.1.0.70100-20.%{rpm_arch}.rpm
Source1: https://%{repository}/%{repoversion}/main/comgr-3.0.0.70100-20.%{rpm_arch}.rpm
Source2: https://%{repository}/%{repoversion}/main/hip-devel-7.1.25424.70100-20.%{rpm_arch}.rpm
Source3: https://%{repository}/%{repoversion}/main/hip-runtime-amd-7.1.25424.70100-20.%{rpm_arch}.rpm
Source4: https://%{repository}/%{repoversion}/main/hipcc-1.1.1.70100-20.%{rpm_arch}.rpm
Source5: https://%{repository}/%{repoversion}/main/hsa-rocr-1.18.0.70100-20.%{rpm_arch}.rpm
Source6: https://%{repository}/%{repoversion}/main/hsa-rocr-devel-1.18.0.70100-20.%{rpm_arch}.rpm
Source7: https://%{repository}/%{repoversion}/main/openmp-extras-devel-20.70.0.70100-20.%{rpm_arch}.rpm
Source8: https://%{repository}/%{repoversion}/main/openmp-extras-runtime-20.70.0.70100-20.%{rpm_arch}.rpm
Source9: https://%{repository}/%{repoversion}/main/rocm-core-7.1.0.70100-20.%{rpm_arch}.rpm
Source10: https://%{repository}/%{repoversion}/main/rocm-dbgapi-0.77.4.70100-20.%{rpm_arch}.rpm
Source11: https://%{repository}/%{repoversion}/main/rocm-device-libs-1.0.0.70100-20.%{rpm_arch}.rpm
Source12: https://%{repository}/%{repoversion}/main/rocm-llvm-20.0.0.25425.70100-20.%{rpm_arch}.rpm
Source13: https://%{repository}/%{repoversion}/main/rocm-smi-lib-7.8.0.70100-20.%{rpm_arch}.rpm
Source14: https://%{repository}/%{repoversion}/main/rocminfo-1.0.0.70100-20.%{rpm_arch}.rpm
Source15: https://%{repository}/%{repoversion}/main/rocprim-devel-4.1.0.70100-20.%{rpm_arch}.rpm
Source16: https://%{repository}/%{repoversion}/main/rocprofiler-2.0.70100.70100-20.%{rpm_arch}.rpm
Source17: https://%{repository}/%{repoversion}/main/rocprofiler-compute-3.3.0.70100-20.%{rpm_arch}.rpm
Source18: https://%{repository}/%{repoversion}/main/rocprofiler-devel-2.0.70100.70100-20.%{rpm_arch}.rpm
Source19: https://%{repository}/%{repoversion}/main/rocprofiler-docs-2.0.70100.70100-20.%{rpm_arch}.rpm
Source20: https://%{repository}/%{repoversion}/main/rocprofiler-plugins-2.0.70100.70100-20.%{rpm_arch}.rpm
Source21: https://%{repository}/%{repoversion}/main/rocprofiler-register-0.6.0.70100-20.%{rpm_arch}.rpm
Source22: https://%{repository}/%{repoversion}/main/rocprofiler-systems-1.2.0.70100-20.%{rpm_arch}.rpm
Source23: https://%{repository}/%{repoversion}/main/hipcub-devel-4.1.0.70100-20.%{rpm_arch}.rpm
Source24: https://%{repository}/%{repoversion}/main/rocthrust-devel-4.1.0.70100-20.%{rpm_arch}.rpm
Source25: https://%{repository}/%{repoversion}/main/hiprand-3.1.0.70100-20.%{rpm_arch}.rpm
Source26: https://%{repository}/%{repoversion}/main/hiprand-devel-3.1.0.70100-20.%{rpm_arch}.rpm
Source27: https://%{repository}/%{repoversion}/main/rocrand-4.1.0.70100-20.%{rpm_arch}.rpm
Source28: https://%{repository}/%{repoversion}/main/rocrand-devel-4.1.0.70100-20.%{rpm_arch}.rpm
Source29: https://%{repository}/%{repoversion}/main/rccl-2.27.7.70100-20.%{rpm_arch}.rpm
Source30: https://%{repository}/%{repoversion}/main/rccl-devel-2.27.7.70100-20.%{rpm_arch}.rpm
Source31: https://%{repository}/%{repoversion}/main/rocshmem-devel-3.0.0.70100-20.%{rpm_arch}.rpm
Source32: https://%{repository}/%{repoversion}/main/rocprofiler-sdk7.1.0-1.0.0.70100-20.%{rpm_arch}.rpm
Source33: https://%{repository}/%{repoversion}/main/rocprofiler-sdk-rocpd7.1.0-1.0.0.70100-20.%{rpm_arch}.rpm
Source34: https://%{repository}/%{repoversion}/main/rocprofiler-sdk-roctx7.1.0-1.0.0.70100-20.%{rpm_arch}.rpm

# sources for rocprofiler-register
Source99: git+https://github.com/ROCm/rocprofiler-register.git?obj=%{rocprofiler_register_branch}/%{rocprofiler_register_tag}&export=%{rocprofiler_register_pkg}&submodules=1&output=/%{rocprofiler_register_pkg}.tgz

BuildRequires: gmake cmake
Requires: numactl zstd fmt
Requires: python3
AutoReq: no

%prep

# unpack rocprofiler-register
mkdir src
tar xavf %{SOURCE99} -C src

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
rpm2cpio %{SOURCE22} | cpio -idmv
rpm2cpio %{SOURCE23} | cpio -idmv
rpm2cpio %{SOURCE24} | cpio -idmv
rpm2cpio %{SOURCE25} | cpio -idmv
rpm2cpio %{SOURCE26} | cpio -idmv
rpm2cpio %{SOURCE27} | cpio -idmv
rpm2cpio %{SOURCE28} | cpio -idmv
rpm2cpio %{SOURCE29} | cpio -idmv
rpm2cpio %{SOURCE30} | cpio -idmv
rpm2cpio %{SOURCE31} | cpio -idmv
rpm2cpio %{SOURCE32} | cpio -idmv
rpm2cpio %{SOURCE33} | cpio -idmv
rpm2cpio %{SOURCE34} | cpio -idmv

# build rocprofiler-register
sed -i -e 's|add_subdirectory(external)|find_package(fmt REQUIRED)\nadd_subdirectory(external)|' src/%{rocprofiler_register_pkg}/CMakeLists.txt
%if %{cms_cxx_standard} != 17
grep -q 'CMAKE_CXX_STANDARD  *17' src/%{rocprofiler_register_pkg}/cmake/rocprofiler_register_options.cmake
sed -i -e  's|CMAKE_CXX_STANDARD  *17|CMAKE_CXX_STANDARD %{cms_cxx_standard}|' src/%{rocprofiler_register_pkg}/cmake/rocprofiler_register_options.cmake
%endif

mkdir -p build/rocprofiler-register
cd build/rocprofiler-register
cmake ../../src/%{rocprofiler_register_pkg} -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} \
  -DCMAKE_VERBOSE_MAKEFILE=TRUE \
  -DROCPROFILER_REGISTER_BUILD_FMT=OFF \
  -DCMAKE_PREFIX_PATH="${FMT_ROOT}"
make all %{makeprocesses}

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

#Create clang cfg file for gcc-toolchain
%if 0%{!?use_system_gcc:1}
host_triple=$(gcc -dumpmachine)
echo "--gcc-toolchain=$GCC_ROOT" > %{i}/llvm/bin/clang++.cfg
echo "--target=$host_triple" >> %{i}/llvm/bin/clang++.cfg
%endif

%post
%if 0%{!?use_system_gcc:1}
%{relocateConfig}/llvm/bin/clang++.cfg
%endif
