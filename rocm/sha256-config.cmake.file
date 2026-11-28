get_filename_component(_sha256_prefix "${CMAKE_CURRENT_LIST_DIR}/../../.." ABSOLUTE)
if(NOT TARGET rocm-sha256)
  add_library(rocm-sha256 STATIC IMPORTED)
  set_target_properties(rocm-sha256 PROPERTIES
    IMPORTED_LOCATION "${_sha256_prefix}/lib/librocm-sha256.a"
    INTERFACE_INCLUDE_DIRECTORIES "${_sha256_prefix}/include"
    INTERFACE_COMPILE_FEATURES cxx_std_17)
  add_library(rocm::sha256 ALIAS rocm-sha256)
endif()
