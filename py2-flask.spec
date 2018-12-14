### RPM external py2-flask 1.0.2
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES} 

Requires: python py2-click py2-jinja2 py2-itsdangerous py2-werkzeug py2-markupsafe

%define pip_name flask

## IMPORT build-with-pip

#%define PipPostBuild \
#   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/lib/python2.7/site-packages/*/*.py
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
