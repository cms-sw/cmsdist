### RPM external triton-inference-client 2.24.0
%define branch r22.07
%define github_user triton-inference-server
%define client_tag a40d66523fc7092835ba863ae0ee85f77e9bd1a2

Source: git+https://github.com/%{github_user}/client.git?obj=%{branch}/%{client_tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: cmake git
Requires: protobuf grpc cuda abseil-cpp re2

%prep

%setup -n %{n}-%{realversion}

%build

# locations of CMakeLists.txt
PROJ_DIR=../%{n}-%{realversion}/src/c++
CML_CPP=${PROJ_DIR}/CMakeLists.txt
CML_LIB=${PROJ_DIR}/library/CMakeLists.txt

# change flag due to bug in gcc10 https://gcc.gnu.org/bugzilla/show_bug.cgi?id=95148
if [[ `gcc --version | head -1 | cut -d' ' -f3 | cut -d. -f1,2,3 | tr -d .` -gt 1000 ]] ; then
    sed -i -e "s|Werror|Wtype-limits|g" ${CML_LIB}
fi

# remove unneeded test libs
sed -i 's/FetchContent_MakeAvailable(googletest)/if(TRITON_ENABLE_TESTS OR TRITON_ENABLE_PERF_ANALYZER)\nFetchContent_MakeAvailable(googletest)\nendif()/' ${CML_CPP}

rm -rf ../build
mkdir ../build
cd ../build

common_tag=38452b707e66eeb590188c9440d257ca3b68f35a
mkdir repo-common && pushd repo-common && curl -k -L https://github.com/%{github_user}/common/archive/${common_tag}.tar.gz | tar -xz --strip=1 && popd

# modifications to common repo (loaded by cmake through FetchContent_MakeAvailable)
COMMON_DIR=$PWD/repo-common
CML_COM=${COMMON_DIR}/CMakeLists.txt
CML_PRB=${COMMON_DIR}/protobuf/CMakeLists.txt

# get shared libraries
sed -i '/^project/a option(BUILD_SHARED_LIBS "Build using shared libraries" ON)' ${CML_COM}

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
    -DTRITON_COMMON_REPO_TAG=${common_tag} \
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
