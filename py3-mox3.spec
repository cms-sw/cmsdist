### RPM external py3-mox3 1.1.0
## IMPORT build-with-pip3

Requires: py3-fixtures py3-pbr
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
