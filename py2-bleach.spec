### RPM external py2-bleach 2.1.2
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}


%define pip_name bleach
Requires: py2-six py2-html5lib 

## IMPORT build-with-pip

