### RPM external py2-xgboost 0.80
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES} 

%define pip_name xgboost

## IMPORT build-with-pip

%define PipPostBuild \
   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/lib/python2.7/site-packages/xgboost/rabit/*/*.py
