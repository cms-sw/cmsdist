### RPM external py2-sympy 1.0
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/isympy
%define pip_name sympy
Requires: py2-mpmath 

## IMPORT build-with-pip

