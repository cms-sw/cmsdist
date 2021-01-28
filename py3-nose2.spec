### RPM external py3-nose2 0.10.0
## IMPORT build-with-pip3

Requires: py3-coverage py3-six

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
