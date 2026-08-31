### RPM external grpc 1.82.0
## INCLUDE cpp-standard

Source: git+https://github.com/grpc/grpc.git?obj=master/v%{realversion}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}.tgz
Source1: https://patch-diff.githubusercontent.com/raw/grpc/grpc/pull/28212.patch
BuildRequires: cmake ninja go
Requires: protobuf zlib pcre c-ares abseil-cpp re2
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
    -DCMAKE_BUILD_TYPE=%{cmake_build_type} \
    -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} \
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
    -DCMAKE_PREFIX_PATH="${PCRE_ROOT};${PROTOBUF_ROOT};${ZLIB_ROOT};${C_ARES_ROOT};${ABSEIL_CPP_ROOT};${RE2_ROOT}"

ninja -v %{makeprocesses}

%install
cd ../build
ninja -v %{makeprocesses} install
ln -sf ../../../abseil-cpp/${ABSEIL_CPP_VERSION}/include/absl %{i}/include/absl


