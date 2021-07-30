### RPM external tbb v2021.3.0

%define tag %{realversion}
%define branch onetbb_2021
%define github_user oneapi-src
%define github_repo oneTBB
Source: git+https://github.com/%{github_user}/%{github_repo}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{branch}-%{tag}.tgz
# ASAN: Use after scope in conformance_concurrent_queue
Source1: https://patch-diff.githubusercontent.com/raw/oneapi-src/oneTBB/pull/435.patch
# Remove arch macros checks for getSmallObjectIndex
Source2: https://patch-diff.githubusercontent.com/raw/oneapi-src/oneTBB/pull/461.patch
Requires: hwloc
BuildRequires: cmake

%prep
%setup -n %{n}-%{realversion}
patch -p1 < %{_sourcedir}/435.patch
patch -p1 < %{_sourcedir}/461.patch

%build
rm -rf %{_builddir}/build
mkdir %{_builddir}/build

cd %{_builddir}/build
cmake ../%{n}-%{realversion} \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_INSTALL_LIBDIR=lib \
  -DCMAKE_HWLOC_2_INCLUDE_PATH=$HWLOC_ROOT/include \
  -DCMAKE_HWLOC_2_LIBRARY_PATH=$HWLOC_ROOT/lib/libhwloc.so \
  -DTBB_CPF=ON

make %{makeprocesses}

%install
cd %{_builddir}/build
make install
