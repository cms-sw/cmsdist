### RPM external py2-hep_ml 0.5.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}


%define pip_name hep_ml
Requires: py2-numpy

## IMPORT build-with-pip



