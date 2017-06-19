### RPM external py2-jupyter_client 5.0.1
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}


%define pip_name jupyter_client
Requires: py2-jupyter_core py2-six py2-traitlets py2-decorator py2-ipython_genutils py2-pyzmq 

## IMPORT build-with-pip
%define PipPostBuild \
   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*

