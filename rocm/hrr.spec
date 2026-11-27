## INCLUDE rocm/flags
### RPM external hrr %{rocm_version_num}
# HIP consumes the shared archive headers; playback requires HIP itself.
%define cmake_args -DHRR_BUILD_PLAYBACK=OFF -DHRR_BUILD_TESTS=OFF
## INCLUDE rocm/systems-build
