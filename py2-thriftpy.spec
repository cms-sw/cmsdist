### RPM external py2-thriftpy 0.3.9
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}

Requires: cython

%define pip_name thriftpy

## IMPORT build-with-pip

#%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
