### RPM external py3-stomp 7.0.0
## IMPORT build-with-pip3

Requires: py3-docopt

%define pip_name stomp.py
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
