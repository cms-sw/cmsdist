### RPM external py2-llvmlite 0.15.0
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
Patch0: py2-llvmlite-static

%define pip_name llvmlite
Requires: py2-enum34 
Requires: llvm

%define PipPreBuild export LLVM_CONFIG=${LLVM_ROOT}/bin/llvm-config && tar -xzf llvmlite-%{realversion}.tar.gz && pushd llvmlite-%{realversion} && for pch in %{patches} ; do patch -p1 < ${pch} ; done && popd && rm -f llvmlite-%{realversion}.tar.gz && tar czf llvmlite-%{realversion}.tar.gz  llvmlite-%{realversion}

## IMPORT build-with-pip

