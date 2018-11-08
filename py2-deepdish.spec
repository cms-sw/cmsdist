### RPM external py2-deepdish 0.3.6
## IMPORT build-with-pip

Requires: py2-tables py2-scipy
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/ddls
