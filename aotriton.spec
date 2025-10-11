### RPM external aotriton 0.10b
## INCLUDE rocm-flags
## INCLUDE microarch_flags

Source: git+https://github.com/ROCm/aotriton?obj=main/%{realversion}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}.tgz
Requires: py3-filelock py3-iniconfig py3-packaging py3-pluggy py3-numpy py3-setuptools py3-wheel py3-pybind11 py3-pandas
Requires: rocm xz
BuildRequires: ninja cmake
Patch1: aotriton-cms

%prep
%setup -n %{n}-%{realversion}
%patch1 -p1

%build
export TRITON_CACHE_DIR=$WORKSPACE/.triton/cache
export TRITON_HOME=$WORKSPACE
rm -rf $TRITON_HOME/.triton && mkdir -p $TRITON_HOME/.triton

rm -rf ../build ; mkdir ../build; cd ../build
cmake ../%{n}-%{realversion} \
 -G Ninja \
 -DCMAKE_BUILD_TYPE=Release \
 -DCMAKE_INSTALL_PREFIX:STRING=%{i} \
 -DAOTRITON_TARGET_ARCH="%{rocm_gpus_cmake}" \
 -DAMDGPU_TARGETS="%{rocm_gpus_cmake}" \
 -DAOTRITON_NO_PYTHON=ON \
 -DVENV_SITE="%{i}/lib/python%{cms_python3_major_minor_version}/site-packages" \
 -DLZMA_LIBRARY_DIRS="${XZ_ROOT}/ilb" \
 -DLZMA_LIBRARIES="${XZ_ROOT}/lib/liblzma.so" \
 -DCMAKE_CXX_FLAGS="-I${XZ_ROOT}/include" \
 -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
 -DCMAKE_VERBOSE=ON \
 -DCMAKE_VERBOSE_MAKEFILE=ON

ninja -v %{makeprocesses}

%install
export TRITON_CACHE_DIR=$WORKSPACE/.triton/cache
export TRITON_HOME=$WORKSPACE
export PYTHONUSERBASE=%{i}
cd ../build
ninja -v %{makeprocesses} install
