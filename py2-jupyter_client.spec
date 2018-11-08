### RPM external py2-jupyter_client 5.2.3
## IMPORT build-with-pip

Requires: py2-jupyter_core py2-tornado py2-python-dateutil py2-pyzmq
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
