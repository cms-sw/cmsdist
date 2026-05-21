### RPM external libzip 1.11.4
Source: https://github.com/nih-at/libzip/releases/download/v%{realversion}/libzip-%{realversion}.tar.gz
BuildRequires: cmake
Requires: zlib zstd
Requires: bz2lib

%prep
%setup -n %{n}-%{realversion}

%build
cmake \
  -S %{_builddir}/%{n}-%{realversion} \
  -B %{_builddir}/build \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_PREFIX_PATH=%{cmake_prefix_path} \
  -DENABLE_COMMONCRYPTO=OFF \
  -DENABLE_GNUTLS=OFF \
  -DENABLE_MBEDTLS=OFF \
  -DENABLE_WINDOWS_CRYPTO=OFF \
  -DBUILD_EXAMPLES=OFF \
  -DBUILD_DOC=OFF

make -C %{_builddir}/build %{makeprocesses}
%install
make -C %{_builddir}/build %{makeprocesses} install