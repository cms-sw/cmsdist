### RPM external py2-bottleneck 1.2.1
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}

%define pip_name bottleneck
Requires: py2-numpy

## IMPORT build-with-pip


