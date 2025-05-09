#End User License Agreement: https://docs.nvidia.com/cuda/eula/index.html
# CUDA/Nvidia libraries
%define cuda_runtime         cudart cudadevrt
%define cuda_fft             cufft cufftw
%define cuda_blas            cublas cublasLt
%define nv_dropin_blas       nvblas
%define cuda_sparse_matrix   cusparse
%define cuda_linear_solver   cusolver
%define cuda_random_number   curand
#Fixme: missing nppicom library in our distribution
%define nv_performance       nppc nppial nppicc nppidei nppif nppig nppim nppist nppisu nppitc npps
%define nv_jpeg              nvjpeg
%define cuda_common          culibos
%define nv_runtime           nvrtc nvrtc-builtins
%define nv_jit               nvJitLink
%define cuda_profile         cupti
%define cuda_tools_ext       nvToolsExt
%define cuda_fileio          cufile cufile_rdma

#Cuda Driver libs
%define cuda_driver          cuda nvidia-ptxjitcompiler nvidia-ml

#Cuda nvvm libs
%define nvvm_libs            nvvm

# Cuda/Nvidia headers
%define nv_runtime_header nvrtc.h
%define cuda_ocupancy     cuda_occupancy.h
%define cuda_fp           \
  cuda_fp16.h cuda_fp16.hpp cuda_bf16.h cuda_bf16.hpp cuda_fp8.h cuda_fp8.hpp cuda_fp6.h cuda_fp6.hpp cuda_fp4.h cuda_fp4.hpp
%define cuda_runtime_headers \
  crt/host_defines.h cuComplex.h cuda_awbarrier_helpers.h cuda_awbarrier_primitives.h cuda_wbarrier.h cuda_pipeline_helpers.h \
  cuda_pipeline_primitives.h cuda_pipeline.h cuda_runtime_api.h cuda.h cuda/std/tuple cuda/std/type_traits cuda/std/type_traits \
  cuda/std/utility device_types.h vector_functions.h vector_types.h
%define cuda_fileio_headers cufile.h

#NVIDIA Common Device Math Functions Library
%define extra_files nvvm/libdevice/libdevice.10.bc

%define all_libs \
  %{?cuda_runtime} %{?cuda_fft} %{?cuda_blas} %{?nv_dropin_blas} %{?cuda_sparse_matrix} %{?cuda_linear_solver} %{?cuda_random_number} \
  %{?nv_performance} %{?nv_jpeg} %{?cuda_common} %{?nv_runtime} %{?nv_optimizing} %{?nv_jit} %{?cuda_profile} %{?cuda_tools_ext} \
  %{?cuda_fileio}

%define runtime_stubs cuda nvidia-ml
%define cuda_incs %{nv_runtime_header} %{cuda_ocupancy} %{cuda_fp} %{cuda_runtime_headers} %{cuda_fileio_headers}

#Helper function to find and install cuda libs
%define find_and_install_lib()                                       \
  if [ -e %{cuda_install_dir}/%{1}/lib${lib}.so ] ; then             \
    cp -P %{cuda_install_dir}/%{1}/lib${lib}.so* %{i}/%{1}/          \
    if [ -e %{cuda_install_dir}/%{1}/lib${lib}_static.a ] ; then     \
      cp -P  %{cuda_install_dir}/%{1}/lib${lib}_static.a %{i}/%{1}/  \
    fi                                                               \
  elif [ -e %{cuda_install_dir}/%{1}/lib${lib}.a ] ; then            \
    cp -P %{cuda_install_dir}/%{1}/lib${lib}.a %{i}/%{1}/            \
  else                                                               \
    echo "ERROR: Unable to find %{1}/lib${lib}"                      \
    exit 1                                                           \
  fi

AutoReq: no
Provides: libnvidia-ml.so.1()(64bit)
Source99: install-cuda.sh
## INCLUDE cuda-version
### RPM external cuda-runtime %{cuda_version}

%install
#Copy runtime libs
mkdir -p %{i}/lib64/stubs %{i}/drivers/lib %{i}/nvvm/lib64
for lib in $(echo "%{all_libs}") ; do
  %find_and_install_lib lib64
done
for lib in $(echo "%{cuda_driver}") ; do
  %find_and_install_lib drivers/lib
done
for lib in $(echo "%{nvvm_libs}") ; do
  %find_and_install_lib nvvm/lib64
done
for x in $(echo "%{extra_files}") ; do
  mkdir -p %{i}/$(dirname ${x})
  cp -P  %{cuda_install_dir}/${x} %{i}/${x}
done

for lib in $(echo "%{runtime_stubs}") ; do
  cp -P %{cuda_install_dir}/lib64/stubs/lib${lib}.so* %{i}/lib64/stubs/
  soname=$(objdump -p %i/lib64/stubs/lib${lib}.so | grep ' SONAME ' | sed "s|.*lib${lib}|lib${lib}|")
  [ -e %{i}/lib64/stubs/${soname} ] || ln -sf lib${lib}.so %{i}/lib64/stubs/${soname}
done

#copy headers
mkdir %i/include
for inc in $(echo "%{cuda_incs}") ; do
  if [ -e %{cuda_install_dir}/include/${inc} ] ; then
    mkdir -p %{i}/include/$(dirname ${inc})
    cp -P %{cuda_install_dir}/include/${inc} %{i}/include/${inc}
  else
    echo "ERROR: No such file: %{cuda_install_dir}/include/${inc}"
  fi
done

#Copy binary/utils
mkdir %i/bin
cp %{cuda_install_dir}/.cms/install-cuda.py %i/bin
cp %{_sourcedir}/install-cuda.sh %i/bin/install-cuda.sh
sed -i -e 's|@CUDA_VERSION@|%{cuda_version}|' %i/bin/install-cuda.sh
