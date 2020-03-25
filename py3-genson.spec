### RPM external py3-genson 1.0.2
## IMPORT build-with-pip3

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
