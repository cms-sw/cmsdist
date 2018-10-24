### RPM external py2-lxml 4.2.5
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
Requires: libxml2 libxslt

## IMPORT build-with-pip
