### RPM external py2-networkx 2.1
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}


%define pip_name networkx
Requires: py2-decorator 

## IMPORT build-with-pip

