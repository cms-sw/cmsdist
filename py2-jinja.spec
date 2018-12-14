### RPM external py2-jinja 2.10
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES} 
Requires: python py2-setuptools
%define pip_name Jinja2
## IMPORT build-with-pip
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
