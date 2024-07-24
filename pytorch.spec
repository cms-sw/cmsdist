### RPM external pytorch 2.3.1
## INCLUDE microarch_flags

%define tag 63d5e9221bedd1546b7d364b5ce4171547db12a9
%define branch cms/v%{realversion}

Source: git+https://github.com/cms-externals/pytorch.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}.tgz
Source1: FindEigen3.cmake
Source2: FindFMT.cmake
Source99: scram-tools.file/tools/eigen/env
Patch1: pytorch-missing-braces
Patch2: pytorch-system-fmt
Patch3: pytorch-cms-aotriton
Patch4: pytorch-hipcc-clang-flags
Patch5: pytorch-rocm-version

BuildRequires: cmake ninja py3-pip
Requires: eigen fxdiv numactl openmpi protobuf psimd python3 py3-PyYAML
Requires: OpenBLAS zlib protobuf fmt py3-pybind11 py3-typing-extensions
Requires: py3-filelock py3-iniconfig py3-packaging py3-packaging py3-pluggy py3-numpy py3-setuptools
%{!?without_rocm:Requires: rocm rocm-rocrand}

%prep
%setup -n %{n}-%{realversion}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
# Pregenerate some files
python3 tools/amd_build/build_amd.py

cp %{_sourcedir}/FindEigen3.cmake %{_sourcedir}/FindFMT.cmake cmake/Modules/
rm -rf ../build && mkdir ../build && cd ../build
source %{_sourcedir}/env

%if 0%{!?without_rocm:1}
# Notice: must be environment variables
export ROCM_PATH=${ROCM_ROOT}
export ROCM_SOURCE_DIR=${ROCM_ROOT}
export PYTORCH_ROCM_ARCH=gfx900,gfx906,gfx908,gfx90a,gfx1030
export PYBIND11_SYSPATH=${PY3_PYBIND11_ROOT}
export TRITON_CACHE_DIR=$WORKSPACE/.triton/cache
export GCC_ROOT=${GCC_ROOT}
hipcc -v
%endif

cmake ../%{n}-%{realversion} \
    -G Ninja \
    -DCMAKE_INSTALL_PREFIX=%{i} \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DBUILD_TEST=OFF \
    -DBUILD_BINARY=OFF \
    -DBUILD_PYTHON=OFF \
    -DUSE_CUDA=OFF \
%if 0%{!?without_rocm:1}
    -DUSE_ROCM=ON \
%endif
    -DUSE_NCCL=OFF \
    -DUSE_FBGEMM=OFF \
    -DUSE_KINETO=OFF \
    -DUSE_MAGMA=OFF \
    -DUSE_METAL=OFF \
    -DUSE_MPS=OFF \
    -DUSE_NNPACK=OFF \
    -DUSE_QNNPACK=OFF \
    -DUSE_PYTORCH_QNNPACK=OFF \
    -DUSE_XNNPACK=OFF \
    -DUSE_NUMA=ON \
    -DNUMA_ROOT_DIR=${NUMACTL_ROOT} \
    -DUSE_NUMPY=OFF \
    -DUSE_OPENMP=ON \
    -DUSE_QNNPACK=OFF \
    -DUSE_VALGRIND=OFF \
    -DUSE_XNNPACK=OFF \
    -DUSE_MKLDNN=OFF \
    -DUSE_DISTRIBUTED=OFF \
    -DUSE_MPI=ON \
    -DUSE_GLOO=OFF \
    -DUSE_TENSORPIPE=OFF \
    -DONNX_ML=ON \
    -DBLAS=OpenBLAS \
    -DBUILD_CUSTOM_PROTOBUF=OFF \
    -DUSE_SYSTEM_EIGEN_INSTALL=ON \
    -DUSE_SYSTEM_PSIMD=ON \
    -DUSE_SYSTEM_FXDIV=ON \
    -DUSE_SYSTEM_PYBIND11=ON \
    -DUSE_SYSTEM_BENCHMARK=ON \
    -DCMAKE_CXX_FLAGS="$CMS_EIGEN_CXX_FLAGS %{selected_microarch}" \
    -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
    -DPYTHON_EXECUTABLE=${PYTHON3_ROOT}/bin/python3

ninja -v  %{makeprocesses}

%install
cd ../build
ninja -v  %{makeprocesses} install

%post
%{relocateConfig}include/caffe2/core/macros.h
%{relocateConfig}share/cmake/ATen/ATenConfig.cmake

# NOTICE: can't build with both cuda and rocm - see aten/CMakeLists.txt
