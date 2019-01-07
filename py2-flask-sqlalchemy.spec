### RPM external py2-flask-sqlalchemy 2.3.2
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES} 

Requires: python py2-flask py2-sqlalchemy

%define pip_name Flask-SQLAlchemy

## IMPORT build-with-pip

#%define PipPostBuild \
#   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/lib/python2.7/site-packages/*/*.py
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
