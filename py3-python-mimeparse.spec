### RPM external py3-python-mimeparse 1.6.0
## IMPORT build-with-pip3

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
