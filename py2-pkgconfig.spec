### RPM external py2-pkgconfig 1.2.2
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}


%define pip_name pkgconfig
Requires: py2-nose

## IMPORT build-with-pip

