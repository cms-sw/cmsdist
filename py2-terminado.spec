### RPM external py2-terminado 0.8.1
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}


%define pip_name terminado
Requires: py2-backportsssl_match_hostname py2-ordereddict py2-tornado py2-six py2-ptyprocess py2-backports_abc py2-singledispatch py2-certifi 

## IMPORT build-with-pip

