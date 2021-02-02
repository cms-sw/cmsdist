### RPM external py3-jsonschema 3.2.0
## IMPORT build-with-pip3

Requires: py3-attrs py3-pyrsistent py3-six
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
