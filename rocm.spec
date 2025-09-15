### RPM external rocm 6.4.3
## INCLUDE cpp-standard
## INITENV SET HIP_PATH %{i}

%if 0%{?rhel} == 7
# allow rpm2cpio dependency on the bootstrap bundle
%undefine drop_bootstrap_lib
%define drop_bootstrap_lib true
%define repository repo.radeon.com/rocm/yum
%else
%define repository repo.radeon.com/rocm/rhel%{rhel}
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

Source0: https://%{repository}/%{repoversion}/main/amd-smi-lib-25.5.1.60403-128.el%{rhel}.%{_arch}.rpm
Source1: https://%{repository}/%{repoversion}/main/comgr-3.0.0.60403-128.el%{rhel}.%{_arch}.rpm
Source2: https://%{repository}/%{repoversion}/main/hip-devel-6.4.43484.60403-128.el%{rhel}.%{_arch}.rpm
Source3: https://%{repository}/%{repoversion}/main/hip-runtime-amd-6.4.43484.60403-128.el%{rhel}.%{_arch}.rpm
Source4: https://%{repository}/%{repoversion}/main/hipcc-1.1.1.60403-128.el%{rhel}.%{_arch}.rpm
Source5: https://%{repository}/%{repoversion}/main/hsa-rocr-1.15.0.60403-128.el%{rhel}.%{_arch}.rpm
Source6: https://%{repository}/%{repoversion}/main/hsa-rocr-devel-1.15.0.60403-128.el%{rhel}.%{_arch}.rpm
Source7: https://%{repository}/%{repoversion}/main/openmp-extras-devel-18.63.0.60403-128.el%{rhel}.%{_arch}.rpm
Source8: https://%{repository}/%{repoversion}/main/openmp-extras-runtime-18.63.0.60403-128.el%{rhel}.%{_arch}.rpm
Source9: https://%{repository}/%{repoversion}/main/rocm-core-6.4.3.60403-128.el%{rhel}.%{_arch}.rpm
Source10: https://%{repository}/%{repoversion}/main/rocm-dbgapi-0.77.2.60403-128.el%{rhel}.%{_arch}.rpm
Source11: https://%{repository}/%{repoversion}/main/rocm-device-libs-1.0.0.60403-128.el%{rhel}.%{_arch}.rpm
Source12: https://%{repository}/%{repoversion}/main/rocm-llvm-19.0.0.25224.60403-128.el%{rhel}.%{_arch}.rpm
Source13: https://%{repository}/%{repoversion}/main/rocm-smi-lib-7.7.0.60403-128.el%{rhel}.%{_arch}.rpm
Source14: https://%{repository}/%{repoversion}/main/rocminfo-1.0.0.60403-128.el%{rhel}.%{_arch}.rpm
Source15: https://%{repository}/%{repoversion}/main/rocprim-devel-3.4.1.60403-128.el%{rhel}.%{_arch}.rpm
Source16: https://%{repository}/%{repoversion}/main/rocprofiler-2.0.60403.60403-128.el%{rhel}.%{_arch}.rpm
Source17: https://%{repository}/%{repoversion}/main/rocprofiler-compute-3.1.1.60403-128.el%{rhel}.%{_arch}.rpm
Source18: https://%{repository}/%{repoversion}/main/rocprofiler-devel-2.0.60403.60403-128.el%{rhel}.%{_arch}.rpm
Source19: https://%{repository}/%{repoversion}/main/rocprofiler-docs-2.0.60403.60403-128.el%{rhel}.%{_arch}.rpm
Source20: https://%{repository}/%{repoversion}/main/rocprofiler-plugins-2.0.60403.60403-128.el%{rhel}.%{_arch}.rpm
Source21: https://%{repository}/%{repoversion}/main/rocprofiler-register-0.4.0.60403-128.el%{rhel}.%{_arch}.rpm
Source22: https://%{repository}/%{repoversion}/main/rocprofiler-systems-1.0.2.60403-128.el%{rhel}.%{_arch}.rpm
Source23: https://%{repository}/%{repoversion}/main/hipcub-devel-3.4.0.60403-128.el%{rhel}.%{_arch}.rpm
Source24: https://%{repository}/%{repoversion}/main/rocthrust-devel-3.3.0.60403-128.el%{rhel}.%{_arch}.rpm
Source25: https://%{repository}/%{repoversion}/main/hiprand-2.12.0.60403-128.el%{rhel}.%{_arch}.rpm
Source26: https://%{repository}/%{repoversion}/main/hiprand-devel-2.12.0.60403-128.el%{rhel}.%{_arch}.rpm
Source27: https://%{repository}/%{repoversion}/main/rocrand-3.3.0.60403-128.el%{rhel}.%{_arch}.rpm
Source28: https://%{repository}/%{repoversion}/main/rocrand-devel-3.3.0.60403-128.el%{rhel}.%{_arch}.rpm
Source29: https://%{repository}/%{repoversion}/main/rccl-2.22.3.60403-128.el%{rhel}.%{_arch}.rpm
Source30: https://%{repository}/%{repoversion}/main/rccl-devel-2.22.3.60403-128.el%{rhel}.%{_arch}.rpm
Source31: https://%{repository}/%{repoversion}/main/rocshmem-devel-2.0.1.60403-128.el%{rhel}.%{_arch}.rpm

# extra sources for pytorch
Source34: https://%{repository}/%{repoversion}/main/hipblas-common-devel-1.0.0.60403-128.el%{rhel}.%{_arch}.rpm
Source35: https://%{repository}/%{repoversion}/main/rocthrust-devel-3.3.0.60403-128.el%{rhel}.%{_arch}.rpm
Source36: https://%{repository}/%{repoversion}/main/hsa-rocr-devel-1.15.0.60403-128.el%{rhel}.%{_arch}.rpm
Source37: https://%{repository}/%{repoversion}/main/rocblas-devel-4.4.1.60403-128.el%{rhel}.%{_arch}.rpm
Source38: https://%{repository}/%{repoversion}/main/rocblas-4.4.1.60403-128.el%{rhel}.%{_arch}.rpm
Source39: https://%{repository}/%{repoversion}/main/hipblas-2.4.0.60403-128.el%{rhel}.%{_arch}.rpm
Source40: https://%{repository}/%{repoversion}/main/hipblas-devel-2.4.0.60403-128.el%{rhel}.%{_arch}.rpm
Source41: https://%{repository}/%{repoversion}/main/hipblaslt-0.12.1.60403-128.el%{rhel}.%{_arch}.rpm
Source42: https://%{repository}/%{repoversion}/main/hipblaslt-devel-0.12.1.60403-128.el%{rhel}.%{_arch}.rpm
Source43: https://%{repository}/%{repoversion}/main/miopen-hip-3.4.0.60403-128.el%{rhel}.%{_arch}.rpm
Source44: https://%{repository}/%{repoversion}/main/miopen-hip-devel-3.4.0.60403-128.el%{rhel}.%{_arch}.rpm
Source45: https://%{repository}/%{repoversion}/main/rocfft-1.0.32.60403-128.el%{rhel}.%{_arch}.rpm
Source46: https://%{repository}/%{repoversion}/main/rocfft-devel-1.0.32.60403-128.el%{rhel}.%{_arch}.rpm
Source47: https://%{repository}/%{repoversion}/main/hipfft-1.0.18.60403-128.el%{rhel}.%{_arch}.rpm
Source48: https://%{repository}/%{repoversion}/main/hipfft-devel-1.0.18.60403-128.el%{rhel}.%{_arch}.rpm
Source49: https://%{repository}/%{repoversion}/main/hipsparse-3.2.0.60403-128.el%{rhel}.%{_arch}.rpm
Source50: https://%{repository}/%{repoversion}/main/hipsparse-devel-3.2.0.60403-128.el%{rhel}.%{_arch}.rpm
Source51: https://%{repository}/%{repoversion}/main/rccl-2.22.3.60403-128.el%{rhel}.%{_arch}.rpm
Source52: https://%{repository}/%{repoversion}/main/rccl-devel-2.22.3.60403-128.el%{rhel}.%{_arch}.rpm
Source53: https://%{repository}/%{repoversion}/main/rocprim-devel-3.4.1.60403-128.el%{rhel}.%{_arch}.rpm
Source54: https://%{repository}/%{repoversion}/main/hipcub-devel-3.4.0.60403-128.el%{rhel}.%{_arch}.rpm
Source55: https://%{repository}/%{repoversion}/main/rocthrust-devel-3.3.0.60403-128.el%{rhel}.%{_arch}.rpm
Source56: https://%{repository}/%{repoversion}/main/hipsolver-2.4.0.60403-128.el%{rhel}.%{_arch}.rpm
Source57: https://%{repository}/%{repoversion}/main/hipsolver-devel-2.4.0.60403-128.el%{rhel}.%{_arch}.rpm
Source58: https://%{repository}/%{repoversion}/main/roctracer-4.1.60403.60403-128.el%{rhel}.%{_arch}.rpm
Source59: https://%{repository}/%{repoversion}/main/roctracer-devel-4.1.60403.60403-128.el%{rhel}.%{_arch}.rpm
Source60: https://%{repository}/%{repoversion}/main/composablekernel-devel6.4.3-1.1.0.60403-128.el%{rhel}.%{_arch}.rpm
Source61: https://%{repository}/%{repoversion}/main/rocsolver-3.28.2.60403-128.el%{rhel}.%{_arch}.rpm
Source62: https://%{repository}/%{repoversion}/main/rocsolver-devel-3.28.2.60403-128.el%{rhel}.%{_arch}.rpm

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

# pytorch
rpm2cpio %{SOURCE34} | cpio -idmv
rpm2cpio %{SOURCE35} | cpio -idmv
rpm2cpio %{SOURCE36} | cpio -idmv
rpm2cpio %{SOURCE37} | cpio -idmv
rpm2cpio %{SOURCE38} | cpio -idmv
rpm2cpio %{SOURCE39} | cpio -idmv
rpm2cpio %{SOURCE40} | cpio -idmv
rpm2cpio %{SOURCE41} | cpio -idmv
rpm2cpio %{SOURCE42} | cpio -idmv
rpm2cpio %{SOURCE43} | cpio -idmv
rpm2cpio %{SOURCE44} | cpio -idmv
rpm2cpio %{SOURCE45} | cpio -idmv
rpm2cpio %{SOURCE46} | cpio -idmv
rpm2cpio %{SOURCE47} | cpio -idmv
rpm2cpio %{SOURCE48} | cpio -idmv
rpm2cpio %{SOURCE49} | cpio -idmv
rpm2cpio %{SOURCE50} | cpio -idmv
rpm2cpio %{SOURCE51} | cpio -idmv
rpm2cpio %{SOURCE52} | cpio -idmv
rpm2cpio %{SOURCE53} | cpio -idmv
rpm2cpio %{SOURCE54} | cpio -idmv
rpm2cpio %{SOURCE55} | cpio -idmv
rpm2cpio %{SOURCE56} | cpio -idmv
rpm2cpio %{SOURCE57} | cpio -idmv
rpm2cpio %{SOURCE58} | cpio -idmv
rpm2cpio %{SOURCE59} | cpio -idmv
rpm2cpio %{SOURCE60} | cpio -idmv
rpm2cpio %{SOURCE61} | cpio -idmv
rpm2cpio %{SOURCE62} | cpio -idmv

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
