### RPM external py3-pymongo 3.9.0
## IMPORT build-with-pip3

Requires: python3

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
