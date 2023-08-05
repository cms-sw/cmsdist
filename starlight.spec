### RPM external starlight r193
## INCLUDE cpp-standard
Requires: clhep

%define branch cms/%{realversion}
%define github_user cms-externals
%define tag e1a5d073144c199aa97d40ff8cbb570b5dc5ed33
Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

Patch0: starlight-r193-allow-setting-CMAKE_CXX_FLAGS

BuildRequires: cmake

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build
rm -rf ../build
mkdir ../build
cd ../build

export CLHEP_PARAM_PATH=${CLHEP_ROOT}
CXXFLAGS="-Wno-error=deprecated-declarations -Wno-error=deprecated-copy -Wno-error=maybe-uninitialized -Wno-error=unused-but-set-variable -std=c++%{cms_cxx_standard}"

cmake ../%{n}-%{realversion} \
 -DCMAKE_INSTALL_PREFIX:PATH="%{i}" \
 -DCMAKE_BUILD_TYPE=Realease \
 -DENABLE_CLHEP=ON \
 -DCMAKE_CXX_FLAGS="$CXXFLAGS"

make %{makeprocesses} VERBOSE=1

%install
cd ../build
make %{makeprocesses} install VERBOSE=1

rm -rf %{i}/lib/archive
