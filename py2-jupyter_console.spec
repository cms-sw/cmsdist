### RPM external py2-jupyter_console 5.2.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}


%define pip_name jupyter_console
Requires: py2-ordereddict py2-ipykernel py2-packaging py2-backports_abc py2-singledispatch py2-pyparsing py2-appdirs py2-pexpect py2-six py2-ptyprocess py2-traitlets py2-ipython_genutils py2-pyzmq py2-pathlib2 py2-tornado py2-jupyter_core py2-ipython py2-certifi py2-pickleshare py2-decorator py2-prompt_toolkit py2-jupyter_client py2-wcwidth py2-Pygments py2-setuptools py2-backportsssl_match_hostname py2-simplegeneric py2-scandir 

## IMPORT build-with-pip


%define PipPostBuild \
   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/jupyter-console

