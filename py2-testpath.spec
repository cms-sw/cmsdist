### RPM external py2-testpath 0.3.1
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

%define PipDownloadOptions --no-deps%%20--no-binary%%3D:none:
%define pip_name testpath

## IMPORT build-with-pip

