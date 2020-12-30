### RPM external tbb master-d86ed7fb

%define tag    %(echo %{realversion} | cut -d- -f 2)
%define branch %(echo %{realversion} | cut -d- -f 1)
%define github_user oneapi-src
Source: git+https://github.com/%{github_user}/oneTBB.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{branch}-%{tag}.tgz
Requires: hwloc
BuildRequires: cmake

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf %{_builddir}/build
mkdir %{_builddir}/build

cd %{_builddir}/build
cmake ../%{n}-%{realversion} \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_INSTALL_LIBDIR=lib \
  -DCMAKE_HWLOC_2_INCLUDE_PATH=$HWLOC_ROOT/include \
  -DCMAKE_HWLOC_2_LIBRARY_PATH=$HWLOC_ROOT/lib/libhwloc.so

make %{makeprocesses}

%install
cd %{_builddir}/build
make install
