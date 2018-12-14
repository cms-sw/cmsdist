### RPM external py2-itsdangerous 1.1.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES} 
Requires: python
%define pip_name itsdangerous
## IMPORT build-with-pip
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
