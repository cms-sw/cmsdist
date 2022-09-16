### RPM external triton-inference-client 2.11.0
%define branch main
%define github_user triton-inference-server
%define tag_2_11_0 36cd3b3c839288c85b15e4df82cfe8fca3fff21b

Source: git+https://github.com/%{github_user}/client.git?obj=%{branch}/%{tag_2_11_0}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Source1: triton-inference-client/model_config.h
Source2: triton-inference-client/model_config.cc
BuildRequires: cmake git
Requires: protobuf grpc cuda abseil-cpp re2

%prep

%setup -n %{n}-%{realversion}

%build

# locations of CMakeLists.txt
PROJ_DIR=../%{n}-%{realversion}/src/c++
CML_CPP=${PROJ_DIR}/CMakeLists.txt
CML_LIB=${PROJ_DIR}/library/CMakeLists.txt

# remove rapidjson dependence
sed -i '/RapidJSON CONFIG REQUIRED/,+13d;' ${CML_LIB}
sed -i '/triton-common-json/d' ${CML_LIB}
# core repo not needed for grpc-client-only install
sed -i '/FetchContent_MakeAvailable(repo-core)/d' ${CML_CPP}
# remove attempts to install external libs
sed -i '\~/../../_deps/repo-third-party-build/~d' ${CML_LIB}
sed -i '\~/../../third-party/~d' ${CML_LIB}
# keep typeinfo in .so by removing ldscript from properties
sed -i '/set_target_properties/,+5d' ${CML_LIB}
# change flag due to bug in gcc10 https://gcc.gnu.org/bugzilla/show_bug.cgi?id=95148
if [[ `gcc --version | head -1 | cut -d' ' -f3 | cut -d. -f1,2,3 | tr -d .` -gt 1000 ]] ; then 
    sed -i -e "s|Werror|Wtype-limits|g" ${CML_LIB}
fi

# these files were extracted from:
# https://github.com/triton-inference-server/server/blob/v2.11.0/src/core/model_config.h
# https://github.com/triton-inference-server/server/blob/v2.11.0/src/core/model_config.cc
cp %{_sourcedir}/model_config.h  ${PROJ_DIR}/library/
cp %{_sourcedir}/model_config.cc ${PROJ_DIR}/library/

# add custom header to cmake build
sed -i 's/grpc_client.cc common.cc/& model_config.cc/' ${CML_LIB}
sed -i 's/grpc_client.h common.h/& model_config.h/' ${CML_LIB}
sed -i '\~${CMAKE_CURRENT_SOURCE_DIR}/common.h~a ${CMAKE_CURRENT_SOURCE_DIR}/model_config.h' ${CML_LIB}

rm -rf ../build
mkdir ../build
cd ../build

common_tag_2_11_0=249232758855cc764c78a12964c2a5c09c388d87
mkdir repo-common && pushd repo-common && curl -k -L https://github.com/%{github_user}/common/archive/${common_tag_2_11_0}.tar.gz | tar -xz --strip=1 && popd

# modifications to common repo (loaded by cmake through FetchContent_MakeAvailable)
COMMON_DIR=$PWD/repo-common
CML_TOP=${COMMON_DIR}/CMakeLists.txt
CML_PRB=${COMMON_DIR}/protobuf/CMakeLists.txt

# remove rapidjson dependence
sed -i '/RapidJSON CONFIG REQUIRED/,+1d;' ${CML_TOP}
sed -i '/JSON utilities/,+17d' ${CML_TOP}
sed -i '/triton-common-json/d' ${CML_TOP}
# remove python dependence
sed -i '/Python REQUIRED COMPONENTS Interpreter/,+10d;' ${CML_PRB}
# change flag due to bug in gcc10 https://gcc.gnu.org/bugzilla/show_bug.cgi?id=95148
if [[ `gcc --version | head -1 | cut -d' ' -f3 | cut -d. -f1,2,3 | tr -d .` -gt 1000 ]] ; then 
    sed -i -e "s|Werror|Wtype-limits|g" ${CML_PRB}
fi

if [ "%{cuda_gcc_support}" = "true" ] ; then
    TRITON_ENABLE_GPU_VALUE=ON
else
    TRITON_ENABLE_GPU_VALUE=OFF
fi

cmake ${PROJ_DIR} \
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
    -DCMAKE_CXX_FLAGS="-Wno-error -fPIC" \
    -DFETCHCONTENT_SOURCE_DIR_REPO-COMMON=${COMMON_DIR} \
    -DCMAKE_PREFIX_PATH="${GRPC_ROOT};${ABSEIL_CPP_ROOT};${RE2_ROOT}"

make %{makeprocesses}

%install
cd ../build
make install

if [ "%{cuda_gcc_support}" = "true" ] ; then
    # modify header for consistent definition of GPU support
    sed -i '/^#ifdef TRITON_ENABLE_GPU/i #define TRITON_ENABLE_GPU' %{i}/include/ipc.h
fi

# remove unneeded
rm %{i}/include/triton/common/triton_json.h
