### RPM external py2-qtconsole 4.4.1
## IMPORT build-with-pip

Requires: py2-ipykernel
%define PipPostBuild \
   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/jupyter-qtconsole
