### RPM external spdlog 1.17.0
Requires: fmt
Source: https://github.com/gabime/spdlog/archive/refs/tags/v%{realversion}.tar.gz
BuildRequires: cmake gmake fmt

%prep
%setup -n spdlog-%{realversion}

%build
cd %{_builddir}
rm -rf build && mkdir build && cd build

cmake ../spdlog-%{realversion} \
    -DCMAKE_INSTALL_PREFIX:STRING=%{i} \
    -DCMAKE_INSTALL_LIBDIR:STRING=lib \
    -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
    -DSPDLOG_BUILD_SHARED=ON \
    -DSPDLOG_BUILD_TESTS=OFF \
    -DSPDLOG_BUILD_EXAMPLE=OFF \
    -DSPDLOG_BUILD_BENCH=OFF \
    -DSPDLOG_FMT_EXTERNAL=ON

make %{makeprocesses}

%install
cd %{_builddir}/build
make install
