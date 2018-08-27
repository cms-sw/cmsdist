### RPM external py2-xgboost 0.72.1
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

%define pip_name xgboost

## IMPORT build-with-pip

%define PipPostBuild \
   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/lib/python2.7/site-packages/xgboost/rabit/*/*.py; \
   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python3|" %{i}/lib/python3.*/site-packages/xgboost/rabit/*/*.py 

