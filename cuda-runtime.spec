%define runtime_libs cublas cublasLt cudart cufft curand nvToolsExt cusolver cusparse nvrtc nvJitLink
%define runtime_stubs nvidia-ml cuda
%define cuda_incs nvrtc.h cufile.h cuda_fp16.h cuda_fp16.hpp cuda_occupancy.h
Source99: install-cuda.sh

## INCLUDE cuda-version
### RPM external cuda-runtime %{cuda_version}

%install
#Copy runtime libs
mkdir -p %i/lib64/stubs
for lib in %runtime_libs ; do
  cp -P %{cuda_install_dir}/lib64/lib${lib}.so* %i/lib64/
done
for lib in %runtime_stubs; do
  cp -P %{cuda_install_dir}/lib64/stubs/lib${lib}.so* %i/lib64/stubs
  soname=$(objdump -p %i/lib64/stubs/lib${lib}.so | grep ' SONAME ' | sed "s|.*lib${lib}|lib${lib}|")
  [ -e %i/lib64/stubs/${soname} ] || ln -sf lib${lib}.so %i/lib64/stubs/${soname}
done

#copy headers
mkdir %i/include
for inc in %{cuda_incs} ; do
  cp -P %{cuda_install_dir}/include/$inc  %i/include/${inc}
done

#Copy binary/utils
mkdir %i/bin
cp %{cuda_install_dir}/.cms/install-cuda.py %i/bin
cp %{_sourcedir}/install-cuda.sh %i/bin/install-cuda.sh
sed -i -e 's|@CUDA_VERSION@|%{cuda_version}|' %i/bin/install-cuda.sh
