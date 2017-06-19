### RPM external py2-jupyter_core 4.3.0
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}


%define pip_name jupyter_core
Requires: py2-ipython_genutils py2-six py2-decorator py2-traitlets 

## IMPORT build-with-pip

%define PipPostBuild \
   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/jupyter-migrate %{i}/bin/jupyter-troubleshoot %{i}/bin/jupyter; rm %{i}/lib/*/site-packages/jupyter.py ; rm %{i}/lib/*/site-packages/jupyter.pyc
