### RPM external py2-jupyter_core 4.4.0
## IMPORT build-with-pip

Requires: py2-traitlets
%define PipPostBuild \
   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/jupyter-migrate %{i}/bin/jupyter-troubleshoot %{i}/bin/jupyter; \
   rm %{i}/lib/*/site-packages/jupyter.py ; \
   rm %{i}/lib/*/site-packages/jupyter.pyc
