### RPM external py2-root_numpy 4.7.3
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

%define doPython3 no

%define pip_name root_numpy
Requires: py2-numpy root

## IMPORT build-with-pip

