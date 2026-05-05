## INCLUDE rocm-config
### RPM external rocm %{rocm_version_num}
## Core runtime  (build this first everything depends on it)
## LLVM-based compiler: amdclang
Requires: rocm-llvm
## HSA runtime (ROCr) + HIP runtime (CLR)
Requires: rocr-runtime
Requires: hip
## Dev utilities version info, CMake helpers, debug agent
Requires: rocm-core rocm-cmake rocminfo rocdbgapi
## Tools observability & systems
## Profiling: SDK (rocprofiler-sdk), compute (omniperf), systems (omnitrace)
Requires: rocprofiler
Requires: rocprofiler-register
Requires: rocprofiler-compute
Requires: rocm-rocprofiler-sdk
Requires: rocm-rocprofiler-systems
## Tracing + AQL packet profiling (rocprofiler-sdk build-time dep)
Requires: roctracer
Requires: aqlprofile
Requires: rocm-smi-lib
Requires: amdsmi
## Inter-GPU communication
Requires: rccl
Requires: rocshmem
## Libraries
Requires: hipblas-common
Requires: hipblas
Requires: rocblas
Requires: hipblaslt
Requires: hipsolver
Requires: rocsolver
Requires: hipsparse
Requires: rocsparse
Requires: hipsparselt
Requires: hipfft
Requires: rocfft
Requires: hiprand
Requires: hipcub
Requires: rocprim
Requires: rocthrust
Requires: miopen
Requires: rocrand
Requires: comgr

%prep
%build
%install
%post
