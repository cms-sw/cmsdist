### RPM external py2-hyperopt 0.1
## IMPORT build-with-pip

Requires: py2-six py2-pymongo py2-nose py2-networkx py2-future py2-pymongo py2-scipy
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
