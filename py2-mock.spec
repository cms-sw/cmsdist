### RPM external py2-mock 2.0.0
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES


%define pip_name mock
Requires: py2-six py2-funcsigs py2-pbr
## IMPORT build-with-pip

