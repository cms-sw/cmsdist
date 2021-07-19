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
