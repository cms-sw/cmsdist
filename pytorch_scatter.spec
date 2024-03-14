### RPM external pytorch_scatter 2.1.2
## INCLUDE compilation_flags
## INCLUDE cpp-standard
%define tag 1824369201e67dd5f06bf71c84b09aab133d2fb1
%define branch cms/v2.1.2

Source: git+https://github.com/valsdav/pytorch_scatter.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}.tgz

BuildRequires: cmake
Requires: pytorch cudnn
%define build_flags -Wall -Wextra -pedantic %{?arch_build_flags} 

%prep
%setup -n %{n}-%{realversion}

%build

rm -rf ../build && mkdir ../build && cd ../build


cmake ../%{n}-%{realversion} \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=%{i} \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
    -DCMAKE_CXX_STANDARD="%{cms_cxx_standard}" \
    -DCMAKE_CXX_FLAGS="%{build_flags}" \
    -DBUILD_TEST=OFF \
    -DWITH_PYTHON=OFF \
    -DWITH_CUDA=OFF \
    -DBUILD_TEST=OFF \
    -DBUILD_SHARED_LIBS=ON

#-DCMAKE_CXX_STANDARD:STRING="%{cms_cxx_standard}" \
   #-DCMAKE_CXX_FLAGS="%{build_flags}" \#-DCMAKE_CXX_STANDARD:STRING="%{cms_cxx_standard}" \
   #-DCMAKE_CXX_FLAGS="%{build_flags}" \

make %{makeprocesses} VERBOSE=1

%install
cd ../build
make %{makeprocesses} install VERBOSE=1

%post
