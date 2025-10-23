### RPM external google-test 1.17.0

BuildRequires: cmake ninja

%define commit 52eb8108c5bdec04579160ae17225d66034bd723
%define branch v1.17.x

%define keep_archives true

Source: git+https://github.com/google/googletest.git?obj=%{branch}/%{commit}&export=googletest-%{realversion}-%{commit}&module=googletest-%{realversion}-%{commit}&output=/googletest-%{realversion}-%{commit}.tgz

%prep
%setup -n googletest-%{realversion}-%{commit}

%build
rm -rf %{_builddir}/build
mkdir -p %{_builddir}/build
cd %{_builddir}/build

cmake ../googletest-%{realversion}-%{commit} \
  -G Ninja \
  -DCMAKE_INSTALL_PREFIX="%{i}" \
  -DCMAKE_CXX_FLAGS="-fPIC" \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_GMOCK=OFF

ninja -v %{makeprocesses}

%install
cd ../build
ninja -v %{makeprocesses} install

%post
%{relocateConfig}lib64/pkgconfig/gtest.pc
%{relocateConfig}lib64/pkgconfig/gtest_main.pc
