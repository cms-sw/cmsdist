### RPM external py2-nbformat 4.4.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}


%define pip_name nbformat
Requires: py2-repozelru py2-argparse py2-six py2-jupyter_core py2-traitlets py2-jsonschema py2-ipython_genutils py2-decorator 

## IMPORT build-with-pip

%define PipPostBuild \
   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/jupyter-trust
