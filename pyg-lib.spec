### RPM external pyg-lib 0.4.0
## INCLUDE compilation_flags
## INCLUDE cpp-standard
## INCLUDE cuda-flags
%define tag 84d48b5553a10d787c730467d4dc4a35bdc380c5
%define branch master
%define github_user pyg-team
Source: git+https://github.com/%{github_user}/pyg-lib.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}.tgz
BuildRequires: cmake
Requires: py3-torch %{!?without_cuda:cuda}
%define build_flags -Wall -Wextra %{?arch_build_flags}
%define cuda_arch_float $(echo %{cuda_arch} | tr ' ' '\\n' | sed -E 's|([0-9])$|.\\1|' | tr '\\n' ' ')
%prep
%setup -n %{n}-%{realversion}
%build
USE_CUDA=OFF
%if 0%{!?without_cuda:1}
if [ "%{cuda_gcc_support}" = "true" ] ; then
USE_CUDA=ON
fi
%endif
rm -rf ../build && mkdir ../build && cd ../build
cmake ../%{n}-%{realversion} \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=%{i} \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
    -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} \
    -DCMAKE_CXX_FLAGS="%{build_flags}" \
    -DBUILD_TEST=OFF \
    -DBUILD_BENCHMARK=OFF \
    -DUSE_PYTHON=OFF \
%if 0%{!?without_cuda:1}
    -DWITH_CUDA=${USE_CUDA} \
    -DTORCH_CUDA_ARCH_LIST="%{cuda_arch_float}" \
    -Dnvtx3_dir=${CUDA_ROOT}/include \
%endif
    -DBUILD_SHARED_LIBS=ON
make %{makeprocesses} VERBOSE=1
%install
cd ../build
mkdir -p %{i}/lib
cp libpyg.so %{i}/lib/
cp third_party/METIS/libmetis/libmetis.so %{i}/lib/
mkdir -p %{i}/include
cp -r ../%{n}-%{realversion}/pyg_lib/csrc %{i}/include/pyg_lib
