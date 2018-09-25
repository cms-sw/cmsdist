### RPM external py2-entrypoints 0.2.3
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

Requires: py2-backports
#there seems to be a source available now - lets try to use it if/when this package gets upgraded
%define PipDownloadOptions --no-deps%%20--no-binary%%3D:none:

## IMPORT build-with-pip

