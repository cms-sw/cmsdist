### RPM external py2-virtualenvwrapper 4.7.2
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}


%define pip_name virtualenvwrapper

## IMPORT build-with-pip

#%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
