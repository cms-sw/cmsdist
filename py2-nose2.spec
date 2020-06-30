### RPM external py2-nose2 0.9.2
## IMPORT build-with-pip

Requires: py2-six py2-coverage py2-mock
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
