### RPM external acts v44.0.1
## INITENV +PATH PYTHON3PATH %{i}/python
## INCLUDE microarch_flags
## INCLUDE cuda-flags
## INCLUDE rocm-flags
## INCLUDE geant4-deps

%define tag         30fb4ea
%define branch      cms/%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
Source99: scram-tools.file/tools/eigen/env

# Build the Acts and Traccc tests
%define build_test 1

BuildRequires: cmake gmake
Requires: boost
Requires: dd4hep
Requires: eigen
Requires: expat
Requires: fastjet
Requires: geant4
Requires: json
Requires: python3
Requires: py3-pybind11
Requires: root
Requires: xerces-c
%{!?without_cuda:Requires: cuda}
%{!?without_rocm:Requires: rocm}
%if %{build_test}
# These are ony used to build the examples and unit tests
Requires: hepmc3
Requires: tbb
# These are used through hepmc3, and need to be available to CMake
Requires: bz2lib
Requires: zlib
Requires: zstd
Requires: xz
%endif

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build
mkdir ../build
cd ../build
source %{_sourcedir}/env

%define cuda_enabled %{?without_cuda:OFF}%{!?without_cuda:ON}
%define rocm_enabled %{?without_rocm:OFF}%{!?without_rocm:ON}

# Notes:
#   - gcc-ar and gcc-ranlib are needed to build static libraries with LTO support.
#   - building with RPATH enabled is necessary to build and run the tests; set CMAKE_SKIP_INSTALL_RPATH to strip the RPATH
#     information after installing the libraries.
#   - HIP/ROCm support is not yet working correctly.

cmake ../%{n}-%{realversion} \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DCMAKE_CXX_COMPILER="$GCC_ROOT/bin/g++" \
  -DCMAKE_CXX_STANDARD="%{cms_cxx_standard}" \
  -DCMAKE_CXX_FLAGS="-fPIC $CMS_EIGEN_CXX_FLAGS %{arch_build_flags} %{selected_microarch} %{lto_build_flags}" \
  -DCMAKE_AR="$GCC_ROOT/bin/gcc-ar" \
  -DCMAKE_RANLIB="$GCC_ROOT/bin/gcc-ranlib" \
  -DCMAKE_BUILD_TYPE="Release" \
  -DCMAKE_INSTALL_PREFIX="%{i}" \
  -DCMAKE_SKIP_INSTALL_RPATH="ON" \
%if 0%{!?without_cuda:1}
  -DCMAKE_CUDA_ARCHITECTURES="$(echo %{cuda_arch} | sed -e 's/ \+/;/g')" \
  -DCMAKE_CUDA_FLAGS="-Wno-deprecated-gpu-targets" \
%endif
%if 0%{!?without_rocm:1}
  -DCMAKE_HIP_ARCHITECTURES="$(echo %{rocm_archs} | sed -e 's/ \+/;/g')" \
  -DAMDGPU_TARGETS="$(echo %{rocm_archs} | sed -e 's/ \+/;/g')" \
%endif
  -DBUILD_SHARED_LIBS="ON" \
  -DACTS_NLOHMANNJSON_SOURCE="" \
  -DACTS_USE_SYSTEM_NLOHMANN_JSON="ON" \
  -DACTS_USE_SYSTEM_PYBIND11="ON" \
  -DACTS_BUILD_PLUGIN_ACTSVG="ON" \
  -DACTS_BUILD_PLUGIN_FASTJET="ON" \
  -DACTS_BUILD_PLUGIN_JSON="ON" \
  -DACTS_BUILD_PLUGIN_ROOT="ON" \
  -DACTS_BUILD_PLUGIN_DD4HEP="ON" \
  -DACTS_BUILD_PLUGIN_GEANT4="ON" \
  -DACTS_BUILD_PLUGIN_TRACCC="ON" \
  -DACTS_ENABLE_LOG_FAILURE_THRESHOLD="ON" \
  -DACTSVG_USE_SYSTEM_PYBIND11="ON" \
  -DCOVFIE_PLATFORM_CPU="ON" \
  -DCOVFIE_PLATFORM_CUDA="%{cuda_enabled}" \
  -DCOVFIE_PLATFORM_HIP="%{rocm_enabled}" \
  -DDETRAY_SETUP_NLOHMANN="ON" \
  -DDETRAY_USE_SYSTEM_NLOHMANN="ON" \
  -DDETRAY_BUILD_HOST="ON" \
  -DDETRAY_BUILD_CUDA="%{cuda_enabled}" \
  -DDETRAY_BUILD_HIP="%{rocm_enabled}" \
  -DTRACCC_BUILD_CUDA="%{cuda_enabled}" \
  -DTRACCC_BUILD_HIP="%{rocm_enabled}" \
  -DTRACCC_SETUP_THRUST="%{cuda_enabled}" \
  -DTRACCC_SETUP_ROCTHRUST="%{rocm_enabled}" \
  -DTRACCC_USE_SYSTEM_THRUST="%{cuda_enabled}" \
  -DTRACCC_USE_SYSTEM_ROCTHRUST="%{rocm_enabled}" \
  -DVECMEM_BUILD_CUDA_LIBRARY="%{cuda_enabled}" \
  -DVECMEM_BUILD_HIP_LIBRARY="%{rocm_enabled}" \
%if %{build_test}
  -DACTS_BUILD_UNITTESTS="ON" \
  -DACTS_BUILD_INTEGRATIONTESTS="ON" \
  -DPython_EXECUTABLE=$(which python3) \
  -DACTS_BUILD_EXAMPLES_PYTHON_BINDINGS="ON" \
  -DTRACCC_BUILD_TESTING="ON" \
  -DCMAKE_GTEST_DISCOVER_TESTS_DISCOVERY_MODE=PRE_TEST \
%endif
  -L

make %{makeprocesses} VERBOSE=1

%install
cd ../build
make install VERBOSE=1

# remove the scripts used to set the Acts environment variables
rm %{i}/bin/this_acts.sh
rm %{i}/bin/this_acts_withdeps.sh
rm %{i}/python/setup.sh

%post
%{relocateConfig}lib64/cmake/*/*.cmake
