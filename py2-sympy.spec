### RPM external py2-sympy 1.3
## IMPORT build-with-pip

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/isympy
Requires: py2-mpmath 
