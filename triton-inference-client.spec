### RPM external triton-inference-client 2.11.0
%define branch main
%define github_user triton-inference-server
%define tag_2_11_0 36cd3b3c839288c85b15e4df82cfe8fca3fff21b

Source: git+https://github.com/%{github_user}/client.git?obj=%{branch}/%{tag_2_11_0}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: cmake git
Requires: protobuf grpc cuda 

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

# extracted from https://github.com/triton-inference-server/server/blob/v2.11.0/src/core/model_config.h
cat << 'EOF' > ${PROJ_DIR}/library/model_config.h
#pragma once

#include <stdint.h>
#include "model_config.pb.h"

namespace nvidia { namespace inferenceserver {

size_t GetDataTypeByteSize(const inference::DataType dtype);

inference::DataType ProtocolStringToDataType(const std::string& dtype);

inference::DataType ProtocolStringToDataType(const char* dtype, size_t len);

}}  // namespace nvidia::inferenceserver
EOF

# extracted from https://github.com/triton-inference-server/server/blob/v2.11.0/src/core/model_config.cc
cat << 'EOF' > ${PROJ_DIR}/library/model_config.cc
#include "model_config.h"

namespace nvidia { namespace inferenceserver {

size_t
GetDataTypeByteSize(const inference::DataType dtype)
{
  switch (dtype) {
    case inference::DataType::TYPE_BOOL:
      return 1;
    case inference::DataType::TYPE_UINT8:
      return 1;
    case inference::DataType::TYPE_UINT16:
      return 2;
    case inference::DataType::TYPE_UINT32:
      return 4;
    case inference::DataType::TYPE_UINT64:
      return 8;
    case inference::DataType::TYPE_INT8:
      return 1;
    case inference::DataType::TYPE_INT16:
      return 2;
    case inference::DataType::TYPE_INT32:
      return 4;
    case inference::DataType::TYPE_INT64:
      return 8;
    case inference::DataType::TYPE_FP16:
      return 2;
    case inference::DataType::TYPE_FP32:
      return 4;
    case inference::DataType::TYPE_FP64:
      return 8;
    case inference::DataType::TYPE_STRING:
      return 0;
    default:
      break;
  }

  return 0;
}

inference::DataType
ProtocolStringToDataType(const std::string& dtype)
{
  return ProtocolStringToDataType(dtype.c_str(), dtype.size());
}

inference::DataType
ProtocolStringToDataType(const char* dtype, size_t len)
{
  if (len < 4 || len > 6) {
    return inference::DataType::TYPE_INVALID;
  }

  if ((*dtype == 'I') && (len != 6)) {
    if ((dtype[1] == 'N') && (dtype[2] == 'T')) {
      if ((dtype[3] == '8') && (len == 4)) {
        return inference::DataType::TYPE_INT8;
      } else if ((dtype[3] == '1') && (dtype[4] == '6')) {
        return inference::DataType::TYPE_INT16;
      } else if ((dtype[3] == '3') && (dtype[4] == '2')) {
        return inference::DataType::TYPE_INT32;
      } else if ((dtype[3] == '6') && (dtype[4] == '4')) {
        return inference::DataType::TYPE_INT64;
      }
    }
  } else if ((*dtype == 'U') && (len != 4)) {
    if ((dtype[1] == 'I') && (dtype[2] == 'N') && (dtype[3] == 'T')) {
      if ((dtype[4] == '8') && (len == 5)) {
        return inference::DataType::TYPE_UINT8;
      } else if ((dtype[4] == '1') && (dtype[5] == '6')) {
        return inference::DataType::TYPE_UINT16;
      } else if ((dtype[4] == '3') && (dtype[5] == '2')) {
        return inference::DataType::TYPE_UINT32;
      } else if ((dtype[4] == '6') && (dtype[5] == '4')) {
        return inference::DataType::TYPE_UINT64;
      }
    }
  } else if ((*dtype == 'F') && (dtype[1] == 'P') && (len == 4)) {
    if ((dtype[2] == '1') && (dtype[3] == '6')) {
      return inference::DataType::TYPE_FP16;
    } else if ((dtype[2] == '3') && (dtype[3] == '2')) {
      return inference::DataType::TYPE_FP32;
    } else if ((dtype[2] == '6') && (dtype[3] == '4')) {
      return inference::DataType::TYPE_FP64;
    }
  } else if (*dtype == 'B') {
    if (dtype[1] == 'Y') {
      if (!strcmp(dtype + 2, "TES")) {
        return inference::DataType::TYPE_STRING;
      }
    } else if (!strcmp(dtype + 1, "OOL")) {
      return inference::DataType::TYPE_BOOL;
    }
  }

  return inference::DataType::TYPE_INVALID;
}

}}  // namespace nvidia::inferenceserver
EOF

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

if [ $(%{cuda_gcc_support}) = true ]; then
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

make %{makeprocesses}

%install
cd ../build
make install

if [ $(%{cuda_gcc_support}) = true ] ; then
    # modify header for consistent definition of GPU support
    sed -i '/^#ifdef TRITON_ENABLE_GPU/i #define TRITON_ENABLE_GPU' %{i}/include/ipc.h
fi

# remove unneeded
rm %{i}/include/triton/common/triton_json.h
