### RPM external py2-xrootdpyfs 0.1.5
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

Requires: xrootd py2-fs py2-typing

## IMPORT build-with-pip
