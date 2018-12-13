### RPM external py2-pycparser 2.19
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES} 
Requires: python
## IMPORT build-with-pip
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*

