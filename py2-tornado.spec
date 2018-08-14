### RPM external py2-tornado 5.1
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}


%define pip_name tornado
Requires: py2-backportsssl_match_hostname py2-ordereddict py2-six py2-backports_abc py2-singledispatch py2-certifi 

## IMPORT build-with-pip

