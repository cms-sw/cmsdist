### RPM external codecompass 1.0
%define github_user cms-externals
Source: https://github.com/%{github_user}/CodeCompass/archive/%{realversion}.tar.gz

BuildRequires: cmake
Requires: thrift odb python sqlite graphviz git java-env boost llvm

%prep
%setup -n CodeCompass-1.0

%build
export CMAKE_PREFIX_PATH=${BOOST_ROOT}:${THRIFT_ROOT}:$CMAKE_PREFIX_PATH
export CMAKE_PREFIX_PATH=${LLVM_ROOT}/share/llvm/cmake:$CMAKE_PREFIX_PATH
export CMAKE_PREFIX_PATH=${ODB_ROOT}:$CMAKE_PREFIX_PATH
export PATH=${THRIFT_ROOT}/bin:$PATH
export PATH=${ODB_ROOT}/bin:$PATH
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=%{i} -DDATABASE=sqlite -DCMAKE_BUILD_TYPE=RelWithDebug ..
make %{makeprocesses}

%install
make install
