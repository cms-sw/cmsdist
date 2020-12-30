### RPM external tbb v2021.1.1

%define tag    %{realversion}
%define branch onetbb_2021
%define github_user oneapi-src
%define github_repo oneTBB
Source: git+https://github.com/%{github_user}/%{github_repo}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{branch}-%{tag}.tgz
# Patch tbb v2021.1.1 CMake file to support $HWLOC_ROOT
# not needed in the tbb master branch
Patch: tbb-2021.1.1-cmake_policy-CMP0074
Requires: hwloc
BuildRequires: cmake

%prep
%setup -n %{n}-%{realversion}
%patch -p1

%build
rm -rf %{_builddir}/build
mkdir %{_builddir}/build

cd %{_builddir}/build
cmake ../%{n}-%{realversion} \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_INSTALL_LIBDIR=lib \
  -DCMAKE_CXX_FLAGS=-Wno-deprecated-copy \
  -DHWLOC_ROOT=$HWLOC_ROOT

make %{makeprocesses}

%install
cd %{_builddir}/build
make install
