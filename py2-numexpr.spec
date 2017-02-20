### RPM external py2-numexpr 2.6.2
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES


%define pip_name numexpr
Requires: py2-numpy 

## IMPORT build-with-pip

