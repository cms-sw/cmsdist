### RPM external py2-mock 2.0.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}


%define pip_name mock
Requires: py2-six py2-funcsigs py2-pbr
## IMPORT build-with-pip

