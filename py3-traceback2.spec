### RPM external py3-traceback2 1.4.0
## IMPORT build-with-pip3

Requires: py3-linecache2
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
