### RPM external py2-llvmlite 0.22.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
#Patch0: py2-llvmlite_lib6

%define pip_name llvmlite
Requires: py2-enum34 
Requires: llvm
BuildRequires: py2-wheel

%define PipPreBuild export LLVM_CONFIG=${LLVM_ROOT}/bin/llvm-config 

## IMPORT build-with-pip

