### RPM external starlight r193
Requires: clhep

%define branch cms/%{realversion}
%define github_user cms-externals
%define tag 689c0da91bacd5591d85d71db0fc7cc6fec0b919
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
CXXFLAGS="-Wno-error=deprecated-declarations -Wno-error=deprecated-copy"

cmake ../%{n}-%{realversion} \
 -DCMAKE_INSTALL_PREFIX:PATH="%{i}" \
 -DCMAKE_BUILD_TYPE=Realease \
 -DENABLE_CLHEP=ON \
 -DCPP11=ON \
 -DCMAKE_CXX_FLAGS="$CXXFLAGS"

make %{makeprocesses} VERBOSE=1

%install
cd ../build
make %{makeprocesses} install VERBOSE=1

rm -rf %{i}/lib/archive
