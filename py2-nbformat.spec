### RPM external py2-nbformat 4.4.0
## IMPORT build-with-pip

Requires: py2-traitlets py2-jsonschema py2-jupyter_core
%define PipPostBuild \
   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/jupyter-trust
