### RPM external xrootd 4.12.9
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
Source: https://github.com/xrootd/xrootd/archive/refs/tags/v%{realversion}.tar.gz

BuildRequires: cmake
Requires: zlib
Requires: openssl
Requires: python
Requires: libuuid

%prep
%setup -n %n-%{realversion}
sed -i -e 's|^ *check_library_exists("uuid" "uuid_generate_random".*$|set(_have_libuuid True)|' cmake/Findlibuuid.cmake

%build
mkdir build
cd build

# By default xrootd has perl, fuse, krb5, readline, and crypto enabled.
# libfuse and libperl are not produced by CMSDIST.
cmake ../ \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DOPENSSL_ROOT_DIR:PATH=${OPENSSL_ROOT} \
  -DZLIB_ROOT:PATH=${ZLIB_ROOT} \
  -DENABLE_PYTHON=FALSE \
  -DENABLE_FUSE=FALSE \
  -DENABLE_KRB5=TRUE \
  -DENABLE_READLINE=FALSE \
  -DENABLE_CRYPTO=TRUE \
  -DCMAKE_SKIP_RPATH=TRUE \
  -DENABLE_PYTHON=TRUE \
  -DCMAKE_CXX_FLAGS="-I${LIBUUID_ROOT}/include" \
  -DCMAKE_SHARED_LINKER_FLAGS="-L${LIBUUID_ROOT}/lib64" \
  -DCMAKE_PREFIX_PATH="${PYTHON_ROOT};${LIBUUID_ROOT}"

# Use makeprocess macro, it uses compiling_processes defined by
# build configuration file or build argument
make %makeprocesses VERBOSE=1

%install
cd build
make install
cd ..

%define strip_files %i/lib
%define keep_archives true

