### RPM external py3-mock 1.3.0
## IMPORT build-with-pip3

Requires: py3-six py3-pbr py3-funcsigs

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
