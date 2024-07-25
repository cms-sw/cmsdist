### RPM external pytorch 2.4.0
## INCLUDE cuda-flags
## INCLUDE microarch_flags

%define cuda_arch_float $(echo %{cuda_arch} | tr ' ' '\\n' | sed -E 's|([0-9])$|.\\1|' | tr '\\n' ' ')

Source: git+https://github.com/pytorch/pytorch.git?obj=main/v%{realversion}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}.tgz
Source1: FindEigen3.cmake
Source2: FindFMT.cmake
Source99: scram-tools.file/tools/eigen/env
Patch1: pytorch-missing-braces
Patch2: pytorch-system-fmt

BuildRequires: cmake ninja
Requires: eigen fxdiv numactl openmpi protobuf psimd python3 py3-PyYAML
Requires: OpenBLAS zlib protobuf fmt py3-pybind11 py3-typing-extensions
%{!?without_cuda:Requires: cuda cudnn}

%prep
%setup -n %{n}-%{realversion}
%patch1 -p1
%patch2 -p1

%build
cp %{_sourcedir}/FindEigen3.cmake %{_sourcedir}/FindFMT.cmake cmake/Modules/
rm -rf ../build && mkdir ../build && cd ../build
source %{_sourcedir}/env

USE_CUDA=OFF
%if 0%{!?without_cuda:1}
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
%if 0%{!?without_cuda:1}
    -DUSE_CUDA=${USE_CUDA} \
    -DTORCH_CUDA_ARCH_LIST="%{cuda_arch_float}" \
    -DCUDNN_INCLUDE_DIR=${CUDNN_ROOT}/include \
    -DCUDNN_LIBRARY=${CUDNN_ROOT}/lib64/libcudnn.so \
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
