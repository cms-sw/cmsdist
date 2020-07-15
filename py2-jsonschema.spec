### RPM external py2-jsonschema 3.2.0
## IMPORT build-with-pip

Requires: py2-functools32 py2-attrs py2-pyrsistent py2-six py2-importlib-metadata
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
