### RPM external triton-inference-client 2.25.0
## INITENV +PATH PYTHON3PATH %{pkginstroot}/${PYTHON3_LIB_SITE_PACKAGES}
## INCLUDE cpp-standard
%define branch r22.08
%define github_user triton-inference-server
%define client_tag b4f10a4650a6c3acd0065f063fd1b9c258f10b73
%define common_tag d5c561841e9bd0818c40e5153bdb88e98725ee79

Source0: git+https://github.com/%{github_user}/client.git?obj=%{branch}/%{client_tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Source1: git+https://github.com/%{github_user}/common.git?obj=%{branch}/%{common_tag}&export=common-%{realversion}&output=/common-%{realversion}.tgz
Patch0: triton-inference-client-uint8
BuildRequires: cmake git py3-wheel
Requires: protobuf grpc abseil-cpp re2 rapidjson
Requires: py3-numpy py3-grpcio-tools py3-python-rapidjson
%{!?without_cuda:Requires: cuda}

%prep

%setup -D -T -b 0 -n %{n}-%{realversion}
%patch0 -p1
sed -i -e 's|import os|import os,sys|' src/python/library/build_wheel.py
%setup -D -T -b 1 -n common-%{realversion}

%build

# locations of CMakeLists.txt
PROJ_DIR=../%{n}-%{realversion}/src/c++
COMMON_DIR=../common-%{realversion}/

rm -rf ../build
mkdir ../build
cd ../build

# modifications to common repo (loaded by cmake through FetchContent_MakeAvailable)
CML_COM=${COMMON_DIR}/CMakeLists.txt

# get shared libraries
sed -i '/^project/a option(BUILD_SHARED_LIBS "Build using shared libraries" ON)' ${CML_COM}

TRITON_ENABLE_GPU_VALUE=%{?without_cuda:OFF}%{!?without_cuda:ON}

cmake ${PROJ_DIR} \
    -DCMAKE_INSTALL_PREFIX="%{i}" \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} \
    -DTRITON_ENABLE_CC_HTTP=OFF \
    -DTRITON_ENABLE_CC_GRPC=ON \
    -DTRITON_ENABLE_PERF_ANALYZER=OFF \
    -DTRITON_ENABLE_EXAMPLES=OFF \
    -DTRITON_ENABLE_TESTS=OFF \
    -DTRITON_USE_THIRD_PARTY=OFF \
    -DTRITON_KEEP_TYPEINFO=ON \
    -DTRITON_COMMON_REPO_TAG=${common_tag} \
    -DTRITON_ENABLE_GPU=${TRITON_ENABLE_GPU_VALUE} \
    -DCMAKE_CXX_FLAGS="-Wno-error -fPIC" \
    -DFETCHCONTENT_SOURCE_DIR_REPO-COMMON=${COMMON_DIR} \
    -DCMAKE_PREFIX_PATH="${GRPC_ROOT};${ABSEIL_CPP_ROOT};${RE2_ROOT};${RAPIDJSON_ROOT}"

make %{makeprocesses} VERBOSE=1

rm -rf ../buildpy ; mkdir ../buildpy ; cd ../buildpy
cmake ../%{n}-%{realversion}/src/python \
    -DCMAKE_INSTALL_PREFIX="%{i}" \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} \
    -DTRITON_ENABLE_PYTHON_HTTP=OFF \
    -DTRITON_ENABLE_PYTHON_GRPC=ON \
    -DTRITON_ENABLE_PERF_ANALYZER=OFF \
    -DTRITON_ENABLE_EXAMPLES=OFF \
    -DTRITON_ENABLE_TESTS=OFF \
    -DTRITON_COMMON_REPO_TAG=${common_tag} \
    -DTRITON_ENABLE_GPU=${TRITON_ENABLE_GPU_VALUE} \
    -DTRITON_VERSION=%{realversion} \
    -DCMAKE_CXX_FLAGS="-Wno-error -Wno-error=sign-compare -Wno-error=deprecated-declarations -fPIC" \
    -DFETCHCONTENT_SOURCE_DIR_REPO-COMMON=${COMMON_DIR} \
    -DCMAKE_PREFIX_PATH="${GRPC_ROOT};${ABSEIL_CPP_ROOT};${RE2_ROOT};${RAPIDJSON_ROOT}"


make %{makeprocesses} VERBOSE=1

%install
cd ../build
make install
cd ../buildpy
mkdir -p %{i}/${PYTHON3_LIB_SITE_PACKAGES}
rsync -a ./library/linux/wheel/build/lib/ %{i}/${PYTHON3_LIB_SITE_PACKAGES}/

if [ "%{cuda_gcc_support}" = "true" ] ; then
    # modify header for consistent definition of GPU support
    sed -i '/^#ifdef TRITON_ENABLE_GPU/i #define TRITON_ENABLE_GPU' %{i}/include/ipc.h
fi

# remove unneeded
rm %{i}/include/triton/common/triton_json.h
