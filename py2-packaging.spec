### RPM external py2-packaging 17.1
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}


%define pip_name packaging
Requires: py2-pyparsing py2-six 

## IMPORT build-with-pip

