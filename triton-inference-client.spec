### RPM external triton-inference-client 2.11.0
%define branch main
%define github_user triton-inference-server
%define tag_2_11_0 36cd3b3c839288c85b15e4df82cfe8fca3fff21b

Source: git+https://github.com/%{github_user}/client.git?obj=%{branch}/%{tag_2_11_0}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: cmake
Requires: protobuf grpc cuda 

%prep

%setup -n %{n}-%{realversion}

%build

# locations of CMakeLists.txt
CML_TOP=../%{n}-%{realversion}/CMakeLists.txt
CML_CPP=../%{n}-%{realversion}/src/c++/CMakeLists.txt
CML_LIB=../%{n}-%{realversion}/src/c++/library/CMakeLists.txt

# remove rapidjson dependence
sed -i '/RapidJSON CONFIG REQUIRED/,+13d;' ${CML_LIB}
sed -i '/triton-common-json/d' ${CML_LIB}
# remove common repo: depends on rapidjson, grpc client doesn't need it
sed -i '/FetchContent_MakeAvailable(repo-common)/d' ${CML_CPP}
# remove attempts to install external libs
sed -i '\~/../../_deps/repo-third-party-build/~d' ${CML_LIB}
sed -i '\~/../../third-party/~d' ${CML_LIB}
sed -i '/-DCURL_DIR:PATH/d' ${CML_TOP}
sed -i 's~-DProtobuf_DIR:PATH~-DProtobuf_DIR:PATH='${PROTOBUF_ROOT}/lib/cmake/protobuf'~' ${CML_TOP}
sed -i 's~-DgRPC_DIR:PATH~-DProtobuf_DIR:PATH='${GRPC_ROOT}/lib/cmake/protobuf'~' ${CML_TOP}
# keep typeinfo in .so by removing ldscript from properties
sed -i '/set_target_properties/,+5d' ${CML_LIB}
# change flag due to bug in gcc10 https://gcc.gnu.org/bugzilla/show_bug.cgi?id=95148
if [[ `gcc --version | head -1 | cut -d' ' -f3 | cut -d. -f1,2,3 | tr -d .` -gt 1000 ]] ; then 
    sed -i -e "s|Werror|Wtype-limits|g" ${CML_LIB}
fi

rm -rf ../build
mkdir ../build
cd ../build

if [ $(%{cuda_gcc_support}) = true ]; then
    TRITON_ENABLE_GPU_VALUE=ON
else
    TRITON_ENABLE_GPU_VALUE=OFF
fi

cmake ../%{n}-%{realversion} \
    -DCMAKE_INSTALL_PREFIX="%{i}" \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DCMAKE_BUILD_TYPE=Release \
    -DTRITON_ENABLE_CC_HTTP=OFF \
    -DTRITON_ENABLE_CC_GRPC=ON \
    -DTRITON_ENABLE_PYTHON_HTTP=OFF \
    -DTRITON_ENABLE_PYTHON_GRPC=OFF \
    -DTRITON_ENABLE_PERF_ANALYZER=OFF \
    -DTRITON_ENABLE_EXAMPLES=OFF \
    -DTRITON_ENABLE_TESTS=OFF \
    -DTRITON_ENABLE_GPU=${TRITON_ENABLE_GPU_VALUE} \
    -DTRITON_VERSION=%{realversion} \
    -DCMAKE_CXX_FLAGS="-Wno-error" \

make %{makeprocesses}

%install
cd ../build
make install

if [ $(%{cuda_gcc_support}) = true ] ; then
    # modify header for consistent definition of GPU support
    sed -i '/^#ifdef TRITON_ENABLE_GPU/i #define TRITON_ENABLE_GPU' %{i}/include/ipc.h
fi

# extra headers needed: model_config.h, model_config.pb.h
