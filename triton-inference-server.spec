### RPM external triton-inference-server 1.12.0
%define branch master
%define github_user NVIDIA

Source: git+https://github.com/%{github_user}/triton-inference-server.git?obj=%{branch}/v%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: cmake
Requires: openssl opencv protobuf grpc curl python py2-wheel py2-setuptools py2-grpcio-tools

%prep

%setup -n %{n}-%{realversion}

%build

# remove config required in cmake
sed -i 's/find_package(CURL CONFIG REQUIRED)/find_package(CURL REQUIRED)/' ../%{n}-%{realversion}/src/clients/c++/library/CMakeLists.txt
# remove perf_client which requires rapidjson
sed -i 's/add_subdirectory(perf_client)//' ../%{n}-%{realversion}/src/clients/c++/CMakeLists.txt

rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion}/build/trtis-clients \
    -DCMAKE_INSTALL_PREFIX="%{i}" \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DCMAKE_BUILD_TYPE=Release \
    -DTRTIS_ENABLE_GPU=OFF \
    -DCURL_LIBRARY=${CURL_ROOT}/lib/libcurl.so \
    -DCURL_INCLUDE_DIR=${CURL_ROOT}/include \
    -DTRTIS_ENABLE_METRICS=OFF \
    -DTRTIS_ENABLE_HTTP_V2=OFF \
    -DTRTIS_ENABLE_GRPC_V2=OFF \
    -DTRTIS_VERSION=%{realversion} \
    -DZLIB_ROOT=${ZLIB_ROOT} \
    -DOPENSSL_ROOT_DIR=${OPENSSL_ROOT} \
    -DCMAKE_PREFIX_PATH="${ZLIB_ROOT}"
make %{makeprocesses}

%install
cd ../build
make install

