### RPM external py3-retry 0.9.1
## IMPORT build-with-pip3

Requires: py3-decorator py3-py
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
