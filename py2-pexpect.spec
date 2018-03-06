### RPM external py2-pexpect 4.4.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}


%define pip_name pexpect
Requires: py2-ptyprocess 

## IMPORT build-with-pip

