### RPM external py2-requests 2.20.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

Requires: py2-urllib3 py2-chardet py2-idna py2-certifi

## IMPORT build-with-pip

