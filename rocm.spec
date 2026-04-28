## INCLUDE rocm-config
### RPM external rocm %{rocm_version_num}
## Core runtime  (build this first everything depends on it)
## LLVM-based compiler: amdclang
## INITENV SET HIP_PATH %{i}
## INITENV SET ROCM_PATH %{i}
## INITENV SET HIP_CLANG_PATH $ROCM_ROOT/lib/llvm/bin
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

%define comp_roots ${ROCM_LLVM_ROOT} ${ROCR_RUNTIME_ROOT} ${HIP_ROOT} ${ROCM_CORE_ROOT} ${ROCM_CMAKE_ROOT} ${ROCMINFO_ROOT} ${ROCDBGAPI_ROOT} ${ROCPROFILER_ROOT} ${ROCPROFILER_REGISTER_ROOT} ${ROCPROFILER_COMPUTE_ROOT} ${ROCM_ROCPROFILER_SDK_ROOT} ${ROCM_ROCPROFILER_SYSTEMS_ROOT} ${ROCTRACER_ROOT} ${AQLPROFILE_ROOT} ${ROCM_SMI_LIB_ROOT} ${AMDSMI_ROOT} ${RCCL_ROOT} ${ROCSHMEM_ROOT} ${HIPBLAS_COMMON_ROOT} ${HIPBLAS_ROOT} ${ROCBLAS_ROOT} ${HIPBLASLT_ROOT} ${HIPSOLVER_ROOT} ${ROCSOLVER_ROOT} ${HIPSPARSE_ROOT} ${ROCSPARSE_ROOT} ${HIPSPARSELT_ROOT} ${HIPFFT_ROOT} ${ROCFFT_ROOT} ${HIPRAND_ROOT} ${HIPCUB_ROOT} ${ROCPRIM_ROOT} ${ROCTHRUST_ROOT} ${MIOPEN_ROOT} ${ROCRAND_ROOT} ${COMGR_ROOT}

# Define the target install area
mkdir -p %{i}
INSTALL_TARGET="%{i}"

for root in %{comp_roots}; do
    if [ -d "$root" ]; then
        echo "Merging $root into $INSTALL_TARGET..."
        # Using -u (update) prevents overwriting newer files with older ones
        # from different component roots
        rsync -au --links "${root}/" "$INSTALL_TARGET/"
    else
        echo "ERROR: Component root not found: $root" >&2
        exit 1
    fi
done
rsync -a --ignore-existing "%{i}/lib64/" "%{i}/lib/"
rm %{i}/lib/llvm/bin/*.cfg
rm -fr '%{i}/lib64/'

ln -r -s -f %{i}/lib %{i}/lib64
ln -r -s -f %{i}/lib/llvm/bin/amdclang     %{i}/bin/
ln -r -s -f %{i}/lib/llvm/bin/amdclang++   %{i}/bin/
ln -r -s -f %{i}/lib/llvm/bin/amdclang-cl  %{i}/bin/
ln -r -s -f %{i}/lib/llvm/bin/amdclang-cpp %{i}/bin/
ln -r -s -f %{i}/lib/llvm/bin/amdflang     %{i}/bin/
ln -r -s -f %{i}/lib/llvm/bin/amdlld       %{i}/bin/

%if 0%{!?use_system_gcc:1}
echo -e "--gcc-toolchain=$GCC_ROOT
--target=$(gcc -dumpmachine)
-m64
-L$GCC_ROOT/lib64
--rocm-path=%{i}
--rocm-device-lib-path=%{i}/amdgcn/bitcode" > %{i}/lib/llvm/bin/clang++.cfg
ln -r -s -f %{i}/lib/llvm/bin/clang++.cfg %{i}/lib/llvm/bin/clang.cfg
%else
echo -e "--rocm-path=%{i}
--rocm-device-lib-path=%{i}/amdgcn/bitcode" > %{i}/lib/llvm/bin/clang++.cfg
ln -r -s -f %{i}/lib/llvm/bin/clang++.cfg %{i}/lib/llvm/bin/clang.cfg
%endif

%post
%{relocateConfig}/lib/llvm/bin/clang++.cfg
