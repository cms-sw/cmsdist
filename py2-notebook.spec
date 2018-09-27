### RPM external py2-notebook 5.6.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}


%define pip_name notebook
Requires: py2-repozelru py2-pandocfilters py2-ordereddict py2-ipykernel py2-packaging py2-backports py2-singledispatch py2-jsonschema py2-pyparsing py2-html5lib py2-appdirs py2-pexpect py2-six py2-ptyprocess py2-traitlets py2-Jinja2 py2-prompt_toolkit py2-nbconvert py2-certifi py2-pyzmq py2-entrypoints py2-pathlib2 py2-terminado py2-nbformat py2-tornado py2-jupyter_core py2-testpath py2-MarkupSafe py2-bleach py2-ipython py2-pickleshare py2-decorator py2-mistune py2-argparse py2-ipython_genutils py2-jupyter_client py2-wcwidth py2-Pygments py2-setuptools py2-backports py2-simplegeneric py2-scandir 

## IMPORT build-with-pip

%define PipPostBuild \
   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
