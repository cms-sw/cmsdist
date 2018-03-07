### RPM external py2-bleach 2.1.2
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}


%define pip_name bleach
Requires: py2-six py2-html5lib 

## IMPORT build-with-pip

