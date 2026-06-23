## INCLUDE rocm-config
### RPM external rocfft %{rocm_version_num}
Requires: hiprand rocm-llvm
Requires: hip rocm-core rocm-llvm rocr-runtime rocm-cmake comgr
%define cmake_args -DROCFFT_BUILD_OFFLINE_TUNER=OFF -DROCFFT_KERNEL_CACHE_ENABLE=OFF
## INCLUDE rocm-libraries-build
