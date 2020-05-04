### RPM external grpc 1.28.1

Source: git+https://github.com/grpc/grpc.git?obj=master/v%{realversion}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}.tgz

BuildRequires: cmake ninja go
Requires: protobuf zlib libunwind openssl
%define keep_archives true

%prep

%setup -n %{n}-%{realversion}

%build

rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
    -G Ninja \
    -DgRPC_INSTALL=ON \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=ON \
    -DgRPC_ABSL_PROVIDER=module \
    -DgRPC_CARES_PROVIDER=module \
    -DgRPC_PROTOBUF_PROVIDER=package \
    -DgRPC_SSL_PROVIDER=package \
    -DgRPC_ZLIB_PROVIDER=package \
    -DZLIB_ROOT=${ZLIB_ROOT} \
    -DCMAKE_INSTALL_PREFIX=%{i} \
    -DCMAKE_PREFIX_PATH="${LIBUNWIND_ROOT};${PROTOBUF_ROOT};${ZLIB_ROOT};${OPENSSL_ROOT}"

ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN)

%install
cd ../build
ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN) install
