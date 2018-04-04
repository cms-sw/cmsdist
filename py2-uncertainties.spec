### RPM external py2-uncertainties 3.0.2
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}


%define pip_name uncertainties
Requires: py2-numpy

## IMPORT build-with-pip



