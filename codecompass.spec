### RPM external codecompass 1.0
%define github_user Ericsson
%define tag a45aaeb300e7739980a8c1814eff65cc477052f6
Source: git+https://github.com/%{github_user}/CodeCompass.git?obj=master/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
BuildRequires: cmake
Requires: thrift odb python sqlite graphviz git java-env boost llvm

%prep
%setup -n codecompass-1.0

%build
export CMAKE_PREFIX_PATH=${BOOST_ROOT}:${THRIFT_ROOT}:$CMAKE_PREFIX_PATH
export CMAKE_PREFIX_PATH=${LLVM_ROOT}/share/llvm/cmake:$CMAKE_PREFIX_PATH
export CMAKE_PREFIX_PATH=${ODB_ROOT}:$CMAKE_PREFIX_PATH
export PATH=${THRIFT_ROOT}/bin:$PATH
export PATH=${ODB_ROOT}/bin:$PATH
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=%{i} -DDATABASE=sqlite -DCMAKE_BUILD_TYPE=RelWithDebug -DPC_LIBTHRIFT_INCLUDE_DIR=${THRIFT_ROOT}/include ..
make %{makeprocesses}

%install
make install
