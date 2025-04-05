### RPM external rocm 6.2.4
## INCLUDE cpp-standard

%if 0%{?rhel} == 7
# allow rpm2cpio dependency on the bootstrap bundle
%undefine drop_bootstrap_lib
%define drop_bootstrap_lib true
%define repository repo.radeon.com/rocm/yum
%else
%define repository repo.radeon.com/rocm/rhel%{rhel}
%endif

# ROCm branch, e.g. 5.6.x, 6.2.x
%define rocm_branch %(echo %{realversion} | cut -d. -f1-2).x

# git branch, tag and directory name for rocprofiler-register
%define rocprofiler_register_branch rocm-%{rocm_branch}
%define rocprofiler_register_tag    rocm-%{realversion}
%define rocprofiler_register_pkg    rocprofiler-register-%{rocprofiler_register_tag}

# AMD repositories are numbered 6.2, 6.2.1, 6.2.2, ..., 6.3
# without any .0 in the directory name
%define repoversion %(echo %{realversion} | sed -e's/\.0$//')
%define baseurl %{repository}/%{repoversion}/main/
%define rpm_version '[0-9]\+\(\.[0-9]\+\)*-[0-9]\+\(\.el%{rhel}\)\?\.%{_arch}'
%define packages            \\\
  amd-smi-lib               \\\
  comgr                     \\\
  hip-devel                 \\\
  hip-runtime-amd           \\\
  hipcc                     \\\
  hipcub-devel              \\\
  hsa-rocr                  \\\
  hsa-rocr-devel            \\\
  openmp-extras-devel       \\\
  openmp-extras-runtime     \\\
  rocm-core                 \\\
  rocm-dbgapi               \\\
  rocm-device-libs          \\\
  rocm-gdb                  \\\
  rocm-llvm                 \\\
  rocm-smi-lib              \\\
  rocminfo                  \\\
  rocprim-devel             \\\
  rocprofiler               \\\
  rocprofiler-devel         \\\
  rocprofiler-plugins       \\\
  rocthrust-devel           \\\
  roctracer                 \\\
  roctracer-devel

# generate the Source statements for the list of packages
%(curl -s %{baseurl} |
  sed -n -e's#<a href="\([^"]*.rpm\)".*#\1#p' |
  grep -v -e '-asan' |
  grep -v -e '-debug' |
  grep -v -e '-rpath' |
  grep -v -F '%{realversion} -' |
  grep "$(for P in %{packages}; do echo -n ^$P-%{rpm_version}.rpm'\|'; done; echo 'do_not_match')" |
  awk '{ printf "Source%d: %s/%s\n", NR-1, "'${baseurl}'", $0; }')

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
# generate the build statements from the list of packages
%(for P in %{packages}; do echo $P; done | awk '{ printf "rpm2cpio %{SOURCE%d} | cpio -idmv\n", NR-1 }')

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

%post
