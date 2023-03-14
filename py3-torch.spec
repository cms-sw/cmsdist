### RPM external py3-torch 1.13.1
### INCLUDE cuda-flags
%define tag %{realversion}
%define branch v1.13.1

Source0: git+https://github.com/pytorch/pytorch.git?obj=%{branch}/v%{tag}&export=%{n}.%{realversion}&submodules=1&output=/%{n}.%{realversion}-%{tag}.tgz
Patch0: py3-torch-cpp-externsion-ppc64.patch

BuildRequires: cmake ninja
Requires: eigen fxdiv numactl openmpi protobuf psimd pthreadpool py3-astunparse py3-cffi py3-future py3-numpy py3-pip py3-protobuf py3-pybind11 py3-pyyaml py3-requests py3-setuptools py3-six py3-tqdm py3-typing-extensions py3-wheel python cuda cudnn rocm

%setup -n %{n}/%{v}
%patch0 -p1

%build
mkdir -p %i

%if "%{?compiling_processes:set}" == "set"
export MAX_JOBS=%compiling_processes
%endif
export COLORIZE_OUTPUT=OFF
export BUILD_TEST=OFF
export USE_CUDA=ON
export TORCH_CUDA_ARCH_LIST=%{cuda_arch_float}

export CUDNN_INCLUDE_DIR=${CUDNN_ROOT}/include
export CUDNN_LIBRARY=${CUDNN_ROOT}/lib64/libcudnn.so

export USE_NCCL=OFF
export USE_FBGEMM=OFF
export USE_KINETO=OFF
export USE_MAGMA=OFF
export USE_METAL=OFF
export USE_MPS=OFF
export USE_BREAKPAD=OFF
export USE_NNPACK=OFF

export USE_NUMA=ON
export NUMA_ROOT_DIR=${NUMACTL_ROOT}

export USE_NUMPY=ON
export USE_OPENMP=ON
export USE_QNNPACK=OFF
export USE_VALGRIND=OFF
export USE_XNNPACK=OFF
export USE_MKLDNN=OFF
export USE_DISTRIBUTED=OFF
export USE_MPI=ON
export USE_GLOO=OFF
export USE_TENSORPIPE=OFF
export ONNX_ML=ON

export PYTORCH_BUILD_VERSION=%{realversion}
export BLAS=OpenBLAS
export WITH_BLAS=open

export BUILD_CUSTOM_PROTOBUF=OFF
export USE_SYSTEM_EIGEN_INSTALL=ON
export pybind11_DIR=${PY3-PYBIND11_ROOT}
export pybind11_INCLUDE_DIR=${PY3-PYBIND11_ROOT}/include
export USE_SYSTEM_PYBIND11=ON

export USE_SYSTEM_PTHREADPOOL=ON
export USE_SYSTEM_PSIMD=ON
export USE_SYSTEM_FXDIV=ON
export USE_SYSTEM_BENCHMARK=ON

%build
# For ROCm -- notice: can't build with both cuda and rocm
# python %{_builddir}/tools/amd_build/build_amd.py
pip3 install --no-clean --no-deps --no-index --no-build-isolation --no-cache-dir --disable-pip-version-check --user -v %{_builddir}
