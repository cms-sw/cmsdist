### RPM external py3-testtools 2.4.0
## IMPORT build-with-pip3

Requires: py3-extras py3-fixtures py3-pbr py3-python-mimeparse py3-six py3-traceback2 py3-unittest2
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
