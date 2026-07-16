### RPM external libzip 1.11.4
Source: https://github.com/nih-at/libzip/releases/download/v%{realversion}/libzip-%{realversion}.tar.gz
BuildRequires: cmake gmake
Requires: zlib zstd xz
Requires: bz2lib


%prep
%setup -n %{n}-%{realversion}

%build
cmake \
  -S %{_builddir}/%{n}-%{realversion} \
  -B %{_builddir}/build \
  -DCMAKE_BUILD_TYPE=%{cmake_build_type} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=%{cmake_build_type} \
  -DCMAKE_PREFIX_PATH=%{cmake_prefix_path} \
  -DENABLE_COMMONCRYPTO=OFF \
  -DENABLE_GNUTLS=OFF \
  -DENABLE_MBEDTLS=OFF \
  -DENABLE_WINDOWS_CRYPTO=OFF \
  -DBUILD_EXAMPLES=OFF \
  -DBUILD_DOC=OFF

make -C %{_builddir}/build %{makeprocesses} VERBOSE=1

%install
make -C %{_builddir}/build %{makeprocesses} install VERBOSE=1

%post
%{relocateConfig}lib64/pkgconfig/libzip.pc
