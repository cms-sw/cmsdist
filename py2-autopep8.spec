### RPM external py2-autopep8 1.4
## IMPORT build-with-pip

Requires: py2-pycodestyle
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
