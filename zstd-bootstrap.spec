### RPM external zstd-bootstrap 1.5.2
%define keep_archives true
Source: https://github.com/facebook/zstd/releases/download/v%{realversion}/zstd-%{realversion}.tar.gz

%prep
%setup -n zstd-%{realversion}

%build

cmake build/cmake \
 -DZSTD_BUILD_CONTRIB:BOOL=OFF \
 -DZSTD_BUILD_STATIC:BOOL=ON \
 -DZSTD_BUILD_SHARED:BOOL=OFF \
 -DZSTD_BUILD_TESTS:BOOL=OFF \
 -DCMAKE_BUILD_TYPE=Release \
 -DZSTD_BUILD_PROGRAMS:BOOL=OFF \
 -DZSTD_LEGACY_SUPPORT:BOOL=OFF \
 -DCMAKE_INSTALL_PREFIX:STRING=%{i} \
 -DCMAKE_INSTALL_LIBDIR:STRING=lib \
 -Dzstd_VERSION:STRING=%{realversion}

make %{makeprocesses} VERBOSE=1

%install

make install
