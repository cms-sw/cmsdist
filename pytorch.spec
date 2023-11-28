### RPM external pytorch 2.1.1
## INCLUDE cuda-flags

%define cuda_arch_float $(echo %{cuda_arch} | tr ' ' '\\n' | sed -E 's|([0-9])$|.\\1|' | tr '\\n' ' ')
%define tag v%{realversion}
%define branch release/2.1

Source: git+https://github.com/pytorch/pytorch.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}.tgz
Source1: FindEigen3.cmake
Source2: FindFMT.cmake
Patch0: pytorch-ignore-different-cuda-include-dir
Patch1: pytorch-missing-braces
Patch2: pytorch-system-fmt

BuildRequires: cmake ninja
Requires: eigen fxdiv numactl openmpi protobuf psimd python3 py3-PyYAML
Requires: cuda cudnn OpenBLAS zlib protobuf fmt py3-pybind11

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cp %{_sourcedir}/FindEigen3.cmake %{_sourcedir}/FindFMT.cmake cmake/Modules/
rm -rf ../build && mkdir ../build && cd ../build

USE_CUDA=OFF
%if "%{cmsos}" != "slc7_aarch64"
if [ "%{cuda_gcc_support}" = "true" ] ; then
USE_CUDA=ON
fi
%endif

cmake ../%{n}-%{realversion} \
    -G Ninja \
    -DCMAKE_INSTALL_PREFIX=%{i} \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DBUILD_TEST=OFF \
    -DBUILD_BINARY=OFF \
    -DBUILD_PYTHON=OFF \
    -DUSE_CUDA=${USE_CUDA} \
    -DTORCH_CUDA_ARCH_LIST="%{cuda_arch_float}" \
    -DCUDNN_INCLUDE_DIR=${CUDNN_ROOT}/include \
    -DCUDNN_LIBRARY=${CUDNN_ROOT}/lib64/libcudnn.so \
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
    -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
    -DPYTHON_EXECUTABLE=${PYTHON3_ROOT}/bin/python3

ninja -v  %{makeprocesses}

%install
cd ../build
ninja -v  %{makeprocesses} install

%post
%{relocateConfig}include/caffe2/core/macros.h
%{relocateConfig}share/cmake/ATen/ATenConfig.cmake

# For ROCm, pre-build
# NOTICE: can't build with both cuda and rocm
# python @{_builddir}/tools/amd_build/build_amd.py
