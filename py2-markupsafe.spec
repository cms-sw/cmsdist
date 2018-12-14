### RPM external py2-MarkupSafe 1.1.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES} 
Requires: python
%define pip_name MarkupSafe
## IMPORT build-with-pip
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
