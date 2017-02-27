### RPM external py2-sympy 1.0
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES


%define pip_name sympy
Requires: py2-mpmath 

## IMPORT build-with-pip

