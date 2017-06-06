### RPM external py2-llvmlite 0.17.1
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}

%define pip_name llvmlite
Requires: py2-enum34 
Requires: llvm

%define PipPreBuild export LLVM_CONFIG=${LLVM_ROOT}/bin/llvm-config

## IMPORT build-with-pip

