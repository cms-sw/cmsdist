### RPM external pytorch-scatter 2.1.2
## INCLUDE compilation_flags
## INCLUDE cpp-standard
%define tag c095c62e4334fcd05e4ac3c4bb09d285960d6be6
%define branch master
%define github_user rusty1s

Source: git+https://github.com/%{github_user}/pytorch_scatter.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}.tgz

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
