### RPM external triton-inference-client 2.20.0
%define branch cmake_fixes_r22.03
%define github_user kpedro88
%define tag_2_20_0 37f6c6dffc81cc40ad9716adb9cc39757afedd7f

Source: git+https://github.com/%{github_user}/client.git?obj=%{branch}/%{tag_2_20_0}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
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

# change version of common repo initially pulled by cmake to avoid inconsistency
sed -i 's~https://github.com/triton-inference-server/common.git~https://github.com/kpedro88/common.git~' ${CML_CPP}
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

common_tag_2_20_0=ccee8e88f397a767c1a7ad9d2fa4491cdcced528
mkdir repo-common && pushd repo-common && curl -k -L https://github.com/%{github_user}/common/archive/${common_tag_2_20_0}.tar.gz | tar -xz --strip=1 && popd

# modifications to common repo (loaded by cmake through FetchContent_MakeAvailable)
COMMON_DIR=$PWD/repo-common
CML_PRB=${COMMON_DIR}/protobuf/CMakeLists.txt

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
    -DTRITON_USE_THIRD_PARTY=OFF \
    -DTRITON_KEEP_TYPEINFO=ON \
    -DTRITON_COMMON_REPO_TAG=${common_tag_2_20_0} \
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
