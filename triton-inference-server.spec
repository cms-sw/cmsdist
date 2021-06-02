### RPM external triton-inference-server 2.3.0
%define branch master
%define github_user triton-inference-server

Source: git+https://github.com/%{github_user}/server.git?obj=%{branch}/v%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: cmake
Requires: opencv protobuf grpc curl python py2-wheel py2-setuptools py2-grpcio-tools python3 cuda

%prep

%setup -n %{n}-%{realversion}

%build

# remove rapidjson dependence
sed -i '/RapidJSON/,+9d;' ../%{n}-%{realversion}/src/core/CMakeLists.txt
sed -i '/triton-json-library/d' ../%{n}-%{realversion}/src/clients/c++/library/CMakeLists.txt
# remove python client because it requires perf_client which is disabled when examples skipped
# if this were enabled, `export PYVER=3` would be needed for build_wheel.sh
sed -i 's~add_subdirectory(../../src/clients/python src/clients/python)~~' ../%{n}-%{realversion}/build/client/CMakeLists.txt
# remove attempts to install external libs
sed -i '\~../../../../..~d' ../%{n}-%{realversion}/src/clients/c++/library/CMakeLists.txt
# keep typeinfo in .so by removing ldscript from properties
sed -i '/set_target_properties/,+5d' ../%{n}-%{realversion}/src/clients/c++/library/CMakeLists.txt
#change flag due to bug in gcc10 https://gcc.gnu.org/bugzilla/show_bug.cgi?id=95148
if [[ `gcc --version | head -1 | cut -d' ' -f3 | cut -d. -f1,2,3 | tr -d .` -gt 1000 ]] ; then 
    sed -i -e "s|Werror|Wtype-limits|g" ../%{n}-%{realversion}/build/client/CMakeLists.txt
fi

rm -rf ../build
mkdir ../build
cd ../build

if [ $(%{cuda_gcc_support}) = true ]; then
    TRITON_ENABLE_GPU_VALUE=ON
else
    TRITON_ENABLE_GPU_VALUE=OFF
fi

cmake ../%{n}-%{realversion}/build/client \
    -DCMAKE_INSTALL_PREFIX="%{i}" \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DCMAKE_BUILD_TYPE=Release \
    -DTRITON_ENABLE_GPU=${TRITON_ENABLE_GPU_VALUE} \
    -DTRITON_CLIENT_SKIP_EXAMPLES=ON \
    -DTRITON_CURL_WITHOUT_CONFIG=ON \
    -DCURL_LIBRARY=${CURL_ROOT}/lib/libcurl.so \
    -DCURL_INCLUDE_DIR=${CURL_ROOT}/include \
    -DTRITON_ENABLE_HTTP=OFF \
    -DTRITON_ENABLE_GRPC=ON \
    -DTRITON_VERSION=%{realversion} \
    -DZLIB_ROOT=${ZLIB_ROOT} \
    -DCMAKE_CXX_FLAGS="-Wno-error" \
    -DCMAKE_PREFIX_PATH="${ZLIB_ROOT}"

make %{makeprocesses}

%install
cd ../build
make install

if [ $(%{cuda_gcc_support}) = true ] ; then
    # modify header for consistent definition of GPU support
    sed -i '/^#ifdef TRITON_ENABLE_GPU/i #define TRITON_ENABLE_GPU' %{i}/include/ipc.h
fi

# extra headers needed
cp src/core/model_config.pb.h %{i}/include/
cp src/core/grpc_service.grpc.pb.h %{i}/include/
cp src/core/grpc_service.pb.h %{i}/include/
