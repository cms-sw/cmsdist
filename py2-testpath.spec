### RPM external py2-testpath 0.3
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES

%define PipDownloadOptions --no-deps%%20--no-binary%%3D:none:
%define pip_name testpath

## IMPORT build-with-pip

