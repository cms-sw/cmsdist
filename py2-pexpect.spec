### RPM external py2-pexpect 4.2.1
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES


%define pip_name pexpect
Requires: py2-ptyprocess 

## IMPORT build-with-pip

