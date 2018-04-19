### RPM external py2-singledispatch 3.4.0.3
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}


%define pip_name singledispatch
Requires: py2-six 

## IMPORT build-with-pip

