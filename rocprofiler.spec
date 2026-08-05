## INCLUDE rocm-config
### RPM external rocprofiler %{rocm_version_num}
#Source1: https://github.com/google/perfetto/archive/eb5ef24c58d13cec289d733d03f0f3f0ed321b12.tar.gz
BuildRequires: py3-barectf py3-CppHeaderParser rocm-cmake
Requires: rocm-core rocr-runtime python3 aqlprofile rocm-hip numactl libxml2 roctracer py3-lxml py3-PyYAML rocm-comgr
%define ROCMPreCMake sed -i '1,7d' %{_builddir}/rocm-systems/projects/%{n}/plugin/perfetto/CMakeLists.txt ; sed -i 's/^set(ROCPROFILER_BUILD_TESTS ON)/set(ROCPROFILER_BUILD_TESTS OFF)/' %{_builddir}/rocm-systems/projects/%{n}/CMakeLists.txt ; sed -i 's/^set(ROCPROFILER_BUILD_CI ON)/set(ROCPROFILER_BUILD_CI OFF)/' %{_builddir}/rocm-systems/projects/%{n}/CMakeLists.txt
%define cmake_args -DGPU_TARGETS="%{rocm_targets}" -DCMAKE_CXX_FLAGS="-I${NUMACTL_ROOT}/include -I${ROCM_CORE_ROOT}/include" -DCMAKE_C_FLAGS="-I${NUMACTL_ROOT}/include -I${ROCM_CORE_ROOT}/include" -DCMAKE_SHARED_LINKER_FLAGS="-L${GCC_ROOT}/lib -L${NUMACTL_ROOT}/lib" -DCMAKE_EXE_LINKER_FLAGS="-L${GCC_ROOT}/lib -L${NUMACTL_ROOT}/lib"
## INCLUDE rocm-systems-build
