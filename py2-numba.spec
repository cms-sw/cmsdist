### RPM external py2-numba 0.36.1
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}


%define pip_name numba
Requires: py2-funcsigs py2-enum34 py2-six py2-singledispatch py2-llvmlite py2-numpy 
%define source_file numba-%{realversion}.tar.gz
%define source0 git+https://github.com/numba/numba?obj=master/f6391886b29b446a9924cbeebd924f53909dd7cc&export=numba-%{realversion}&output=/source.tar.gz

## IMPORT build-with-pip

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
