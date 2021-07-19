#pragma once

#include <stdint.h>
#include "model_config.pb.h"

namespace nvidia { namespace inferenceserver {

size_t GetDataTypeByteSize(const inference::DataType dtype);

inference::DataType ProtocolStringToDataType(const std::string& dtype);

inference::DataType ProtocolStringToDataType(const char* dtype, size_t len);

}}  // namespace nvidia::inferenceserver
