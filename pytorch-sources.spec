### RPM external pytorch-sources 2.8.0
## INCLUDE rocm-flags
## INCLUDE microarch_flags
# rebuild 1

# %define cuda_arch_float $(echo %{cuda_arch} | tr ' ' '\\n' | sed -E 's|([0-9])$|.\\1|' | tr '\\n' ' ' | sed -e's/ *$/+PTX/')

Source: git+https://github.com/pytorch/pytorch.git?obj=main/v%{realversion}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}.tgz
Source1: FindEigen3.cmake
Source99: scram-tools.file/tools/eigen/env
Patch1: pytorch-missing-braces
Patch2: pytorch-system-fmt
Patch3: pytorch-kineto-fmt

BuildRequires: cmake ninja
Requires: eigen fxdiv numactl protobuf psimd python3 py3-PyYAML py3-pip xz aotriton
Requires: OpenBLAS zlib protobuf fmt py3-pybind11 py3-typing-extensions
Requires: py3-filelock py3-iniconfig py3-packaging py3-packaging py3-pluggy py3-numpy py3-setuptools
# %{!?without_cuda:Requires: cuda cudnn} -- TODO
%{!?without_rocm:Requires: rocm}

%prep
%setup -n %{n}-%{realversion}
%patch1 -p1
%patch2 -p1
%patch3 -p0

%build
# Pregenerate some files
python3 tools/amd_build/build_amd.py

cp %{_sourcedir}/FindEigen3.cmake cmake/Modules/
source %{_sourcedir}/env

# Notice: must be environment variables
export USE_CUDA=OFF
export ROCM_PATH=${ROCM_ROOT}
export ROCM_SOURCE_DIR=${ROCM_ROOT}
export AMDGPU_TARGETS="$(echo '%{rocm_archs}' | sed -e 's/,/ /g')"
export PYTORCH_ROCM_ARCH="%{rocm_archs}"
export PYBIND11_SYSPATH=${PY3_PYBIND11_ROOT}
export AOTRITON_INSTALLED_PREFIX=${AOTRITON_ROOT}
export GCC_ROOT=${GCC_ROOT}
export LibLZMA_ROOT=${XZ_ROOT}
export CMAKE_VERBOSE=ON
export USE_SYSTEM_LIBS=OFF
export USE_SYSTEM_PSIMD=ON
export PSIMD_SOURCE_DIR=${PSIMD_ROOT}

export BUILD_TEST=OFF
export BUILD_BINARY=OFF
export BUILD_PYTHON=ON
export USE_CUDA=OFF
export USE_CUDNN=OFF
export USE_CUSPARSELT=OFF
export USE_CUDSS=OFF
export USE_NCCL=OFF
export USE_ROCM=ON
export USE_XPU=OFF
export USE_FBGEMM=OFF
export USE_KINETO=OFF
export USE_MAGMA=OFF
export USE_MPS=OFF
export USE_NNPACK=OFF
export USE_QNNPACK=OFF
export USE_PYTORCH_QNNPACK=OFF
export USE_XNNPACK=OFF
export USE_NUMA=ON
export NUMA_ROOT_DIR=${NUMACTL_ROOT}
export USE_NUMPY=OFF
export USE_OPENMP=OFF
export USE_QNNPACK=OFF
export USE_VALGRIND=OFF
export USE_XNNPACK=OFF
export USE_MKLDNN=OFF
export USE_DISTRIBUTED=OFF
export USE_MPI=ON
export USE_GLOO=OFF
export USE_TENSORPIPE=OFF
export ONNX_ML=ON
export BLAS=OpenBLAS
export BUILD_CUSTOM_PROTOBUF=OFF
export USE_SYSTEM_EIGEN_INSTALL=ON
export USE_SYSTEM_PSIMD=ON
export USE_SYSTEM_FXDIV=ON
export USE_SYSTEM_PYBIND11=ON
export USE_SYSTEM_BENCHMARK=ON
export CMAKE_CXX_FLAGS="$CMS_EIGEN_CXX_FLAGS %{selected_microarch}"
export CMAKE_PREFIX_PATH="%{cmake_prefix_path}"
export LIBLZMA_ROOT=${XZ_ROOT}
export PYTHON_EXECUTABLE=${PYTHON3_ROOT}/bin/python3
export BUILD_LIBTORCH_WHL=ON

python3 setup.py bdist_wheel

%install
cp %{_builddir}/%{n}-%{realversion}/dist/*.whl %{i}/torch-%{realversion}-cp%{cms_python3_major_minor}-cp%{cms_python3_major_minor}-linux_%{_arch}.whl
# The wheel file is named like torch-2.7.1a0+gitunknown-cp39-cp39-linux_x86_64.whl, make the name more predictable

# NOTICE: can't build with both cuda and rocm - see aten/CMakeLists.txt
