### RPM external py2-llvmlite 0.20.0
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
#Patch0: py2-llvmlite_lib6

%define pip_name llvmlite

Requires: py2-enum34 
Requires: llvm
BuildRequires: py2-wheel
%define PipPreBuild export LLVM_CONFIG=${LLVM_ROOT}/bin/llvm-config 
%define source_file llvmlite-%{realversion}.tar.gz
%define source0     git+https://github.com/numba/llvmlite?obj=master/772b6099e43017d58793bbed6b3ca5bb1dbdca32&export=llvmlite-%{realversion}&output=/source.tar.gz

## IMPORT build-with-pip

