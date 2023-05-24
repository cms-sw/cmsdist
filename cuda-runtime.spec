%define runtime_libs cublas cublasLt cudart cufft curand nvToolsExt
%define runtime_stubs nvidia-ml cuda
Source99: install-cuda.sh

## INCLUDE cuda-version
### RPM external cuda-runtime %{cuda_version}

%install
mkdir -p %i/lib64/stubs
for lib in %runtime_libs ; do
  cp -P %{cuda_install_dir}/lib64/lib${lib}.so* %i/lib64/
done
for lib in %runtime_stubs; do
  cp -P %{cuda_install_dir}/lib64/stubs/lib${lib}.so* %i/lib64/stubs
done
mkdir %i/bin
cp %{cuda_install_dir}/.cms/install-cuda.py %i/bin
cp %{_sourcedir}/install-cuda.sh %i/bin/install-cuda.sh
sed -i -e 's|@CUDA_VERSION@|%{cuda_version}|' %i/bin/install-cuda.sh
