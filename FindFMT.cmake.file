# Find FMT
#
# Find the FMT includes
# 
# if you nee to add a custom library search path, do it via via CMAKE_PREFIX_PATH 
# 
# This module defines
#  FMT_INCLUDE_DIRS, where to find header, etc.
#  FMT_FOUND, If false, do not try to use FMT.

# only look in default directories
find_path(
  FMT_INCLUDE_DIR
  NAMES fmt/core.h
  DOC "FMT include dir"
  HINTS ${FMT_ROOT}/include
)

if (NOT FMT_INCLUDE_DIR)
  MESSAGE(FATAL_ERROR "Error, FMT include dir not found. Did you set FMT_ROOT variable?")
endif()

set(FMT_INCLUDE_DIRS ${FMT_INCLUDE_DIR})

# handle the QUIETLY and REQUIRED arguments and set FMT_FOUND to TRUE
# if all listed variables are TRUE, hide their existence from configuration view
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(FMT DEFAULT_MSG FMT_INCLUDE_DIR)
mark_as_advanced (FMT_FOUND FMT_INCLUDE_DIR)
