### RPM external py2-nbdime 1.0.2
## IMPORT build-with-pip

Requires: py2-notebook py2-GitPython py2-requests py2-colorama py2-backports
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*


