### RPM external glog 0.7.1
Source0: https://github.com/google/glog/archive/refs/tags/v%{realversion}.tar.gz

%prep
%setup -n glog-%{realversion}

%build
mkdir -p ../build && cd ../build

cmake ../%{n}-%{realversion} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_CXX_STANDARD=17 \
  -DBUILD_SHARED_LIBS=ON \
  -DWITH_GTEST=OFF \
  -DWITH_GFLAGS=OFF \
  -DWITH_UNWIND=OFF

make %{makeprocesses}
%install
make -C %{_builddir}/build  install
