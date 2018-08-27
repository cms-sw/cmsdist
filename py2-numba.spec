### RPM external py2-numba 0.39.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}


%define pip_name numba
Requires: py2-funcsigs py2-enum34 py2-six py2-singledispatch py2-llvmlite py2-numpy 
%define source_file numba-%{realversion}.tar.gz
%define source0 git+https://github.com/numba/numba?obj=master/9ed665ea67ce293b94c641aab0387fc846588b38&export=numba-%{realversion}&output=/source.tar.gz


## IMPORT build-with-pip

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
