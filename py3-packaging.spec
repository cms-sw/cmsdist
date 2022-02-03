### RPM external py3-packaging 21.3
## IMPORT build-with-pip3
Requires: py3-pyparsing 

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
