### RPM external py2-entrypoints 0.2.2
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES

%define PipDownloadOptions --no-deps%%20--no-binary%%3D:none:
%define pip_name entrypoints


## IMPORT build-with-pip

