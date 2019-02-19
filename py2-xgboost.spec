### RPM external py2-xgboost 0.80
## IMPORT build-with-pip

Requires: py2-scipy
%define PipPostBuild \
   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/lib/python2.7/site-packages/xgboost/rabit/*/*.py
