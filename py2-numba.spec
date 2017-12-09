### RPM external py2-numba 0.36.1
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}


%define pip_name numba
Requires: py2-funcsigs py2-enum34 py2-six py2-singledispatch py2-llvmlite py2-numpy 


## IMPORT build-with-pip

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
