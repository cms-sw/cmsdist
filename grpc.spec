### RPM external grpc 1.33.1-patches

%define tag b54a5b338637f92bfcf4b0bc05e0f57a5fd8fadd
Source: git+https://github.com/grpc/grpc.git?obj=master/%{tag}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}.tgz
Patch0: grpc-ssl-fix
Patch1: grpc-gcc11
BuildRequires: cmake ninja go
Requires: protobuf zlib pcre c-ares abseil-cpp re2
%define keep_archives true

%prep

%setup -n %{n}-%{realversion}
if [ ! -z "$OPENSSL_ROOT" ]; then
%patch0 -p1
fi
%patch1 -p1

%build
rm -rf ../build
mkdir ../build
cd ../build
OPENSSLROOT=""
if [ ! -z "$OPENSSL_ROOT" ]; then OPENSSLROOT=";${OPENSSL_ROOT}" ; fi

cmake ../%{n}-%{realversion} \
    -G Ninja \
    -DgRPC_INSTALL=ON \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_CXX_STANDARD=17 \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DgRPC_ABSL_PROVIDER=package \
    -DgRPC_CARES_PROVIDER=package \
    -DgRPC_PROTOBUF_PROVIDER=package \
    -DgRPC_SSL_PROVIDER=package \
    -DgRPC_ZLIB_PROVIDER=package \
    -DgRPC_RE2_PROVIDER=package \
    -DZLIB_ROOT=${ZLIB_ROOT} \
    -DCMAKE_INSTALL_PREFIX=%{i} \
    -DCMAKE_PREFIX_PATH="${PCRE_ROOT};${PROTOBUF_ROOT};${ZLIB_ROOT}${OPENSSLROOT};${C_ARES_ROOT};${ABSEIL_CPP_ROOT};${RE2_ROOT}"

ninja -v %{makeprocesses}

%install
cd ../build
ninja -v %{makeprocesses} install
