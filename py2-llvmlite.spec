### RPM external py2-llvmlite 0.23.2
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

%define pip_name llvmlite
Requires: py2-enum34 
Requires: llvm
BuildRequires: py2-wheel

%define PipPreBuild export LLVM_CONFIG=${LLVM_ROOT}/bin/llvm-config 
%define source_file llvmlite-%{realversion}.tar.gz
%define source0     git+https://github.com/numba/llvmlite?obj=master/9ae78b184965f76d32b2120c25216cabe23bb3c4&export=llvmlite-%{realversion}&output=/source.tar.gz

## IMPORT build-with-pip
