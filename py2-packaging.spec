### RPM external py2-packaging 16.8
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}


%define pip_name packaging
Requires: py2-pyparsing py2-six 

## IMPORT build-with-pip

