### RPM external py2-entrypoints 0.2.3
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}

%define PipDownloadOptions --no-deps%%20--no-binary%%3D:none:
%define pip_name entrypoints


## IMPORT build-with-pip

