### RPM external google-benchmark 1.9.4

BuildRequires: cmake ninja

%define commit eddb0241389718a23a42db6af5f0164b6e0139af
%define branch main

%define keep_archives true

Source: git+https://github.com/google/benchmark.git?obj=%{branch}/%{commit}&export=benchmark-%{realversion}-%{commit}&module=benchmark-%{realversion}-%{commit}&output=/benchmark-%{realversion}-%{commit}.tgz

%prep
%setup -n benchmark-%{realversion}-%{commit}

%build
rm -rf %{_builddir}/build
mkdir -p %{_builddir}/build
cd %{_builddir}/build

cmake ../benchmark-%{realversion}-%{commit} \
  -G Ninja \
  -DCMAKE_INSTALL_PREFIX="%{i}" \
  -DCMAKE_CXX_FLAGS="-fPIE" \
  -DCMAKE_BUILD_TYPE=Release \
  -DBENCHMARK_ENABLE_GTEST_TESTS=OFF \
  -DBENCHMARK_DOWNLOAD_DEPENDENCIES=OFF

ninja -v %{makeprocesses}

%install
cd ../build
ninja -v %{makeprocesses} install

%post
%{relocateConfig}lib64/pkgconfig/benchmark.pc
