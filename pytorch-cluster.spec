### RPM external pytorch-cluster 1.6.3
## INCLUDE compilation_flags
## INCLUDE cpp-standard
%define tag f2d99195a0003ca2d2ba9ed50d0117e2f23360e0
%define branch cms/v1.6.3
%define github_user valsdav

Source: git+https://github.com/%{github_user}/pytorch_cluster.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}.tgz

BuildRequires: cmake
Requires: pytorch cudnn
%define build_flags -Wall -Wextra -pedantic %{?arch_build_flags} 

%prep
%setup -n %{n}-%{realversion}
# Make sure the default c++sdt stand is c++11
grep -q 'CMAKE_CXX_STANDARD  *14' CMakeLists.txt
sed -i -e 's|CMAKE_CXX_STANDARD  *14|CMAKE_CXX_STANDARD %{cms_cxx_standard}|' CMakeLists.txt

%build

rm -rf ../build && mkdir ../build && cd ../build


cmake ../%{n}-%{realversion} \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=%{i} \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
    -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} \
    -DCMAKE_CXX_FLAGS="%{build_flags}" \
    -DBUILD_TEST=OFF \
    -DWITH_PYTHON=OFF \
    -DWITH_CUDA=OFF \
    -DBUILD_TEST=OFF \
    -DBUILD_SHARED_LIBS=ON 


make %{makeprocesses} VERBOSE=1

%install
cd ../build
make %{makeprocesses} install VERBOSE=1

%post
