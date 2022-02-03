### RPM external py3-mongomock 4.0.0
## IMPORT build-with-pip3
Requires: py3-packaging py3-sentinels py3-six

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
