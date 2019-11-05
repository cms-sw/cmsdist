### RPM external py3-stomp 4.1.22
## IMPORT build-with-pip3

Requires: python3 py2-setuptools

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
