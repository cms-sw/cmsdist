### RPM external py2-pickleshare 0.7.4
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}


%define pip_name pickleshare
Requires: py2-six py2-pathlib2 py2-scandir 

## IMPORT build-with-pip

