### RPM external cuda-api-wrappers 20180503
%define tag 301361e7b20369e6d72bc078a2148c2b64eb1e4d
%define branch master
%define github_user cms-externals

Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Requires: cuda
BuildRequires: cmake
AutoReqProv: no

# include .a files
%define keep_archives true

%prep
%setup -q -n %{n}-%{realversion}

%build
mkdir build
cd build
cmake .. \
  -DCUDA_TOOLKIT_ROOT_DIR=$CUDA_ROOT \
  -DCUDA_SEPARABLE_COMPILATION=ON \
  -DCUDA_TARGET_COMPUTE_CAPABILITY=50 \
  -DCUDA_NVCC_FLAGS=-O2
make VERBOSE=1

%install
find src/ -name '*.cpp' -delete
cp -ar src       %{i}/include
cp -ar build/lib %{i}/lib
