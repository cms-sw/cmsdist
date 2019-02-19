### RPM external py2-gunicorn 19.9.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES} 

Requires: python

%define pip_name gunicorn

## IMPORT build-with-pip

#%define PipPostBuild \
#   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/lib/python2.7/site-packages/*/*.py
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
