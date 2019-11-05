### RPM external py3-py4j 0.10.8.1
## IMPORT build-with-pip3

Requires: python3 py2-setuptools

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
