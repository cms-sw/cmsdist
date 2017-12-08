### RPM external py2-llvmlite 0.21.0
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
#Patch0: py2-llvmlite_lib6

%define pip_name llvmlite
Requires: py2-enum34 
Requires: llvm
BuildRequires: py2-wheel

%define PipPreBuild export LLVM_CONFIG=${LLVM_ROOT}/bin/llvm-config 
%define source_file llvmlite-%{realversion}.tar.gz
%define source0     git+https://github.com/numba/llvmlite?obj=master/b993afd8dcbcf07a60f145c6f25b0c9c96772c5d&export=llvmlite-%{realversion}&output=/source.tar.gz

## IMPORT build-with-pip

