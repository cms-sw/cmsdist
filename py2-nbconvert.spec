### RPM external py2-nbconvert 5.4.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}


%define pip_name nbconvert
Requires: py2-mistune py2-argparse py2-entrypoints py2-pandocfilters py2-traitlets py2-nbformat py2-jupyter_core py2-testpath py2-repozelru py2-six py2-MarkupSafe py2-Pygments py2-Jinja2 py2-jsonschema py2-bleach py2-ipython_genutils py2-html5lib py2-decorator 

## IMPORT build-with-pip

%define PipPostBuild \
   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/jupyter-nbconvert
