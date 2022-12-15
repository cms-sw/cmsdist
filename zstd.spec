### RPM external zstd 1.5.2
## INITENV SETV ZSTD_SOURCE %{source0}
## INITENV SETV ZSTD_STRIP_PREFIX %{source_prefix}

%define source0 https://github.com/facebook/zstd/releases/download/v%{realversion}/zstd-%{realversion}.tar.gz
%define source_prefix %{n}-%{realversion}
Source: %{source0}

BuildRequires: gmake cmake

%prep
%setup -n %{source_prefix}

%build

cmake build/cmake \
 -DZSTD_BUILD_CONTRIB:BOOL=OFF \
 -DZSTD_BUILD_STATIC:BOOL=OFF \
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
