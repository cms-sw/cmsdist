### RPM external py2-hyperopt 0.1
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}

Requires: py2-numpy py2-scipy

%define pip_name hyperopt


## IMPORT build-with-pip

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
