### RPM external py2-pkgconfig 1.3.1
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}


%define pip_name pkgconfig
Requires: py2-nose

## IMPORT build-with-pip

