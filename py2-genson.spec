### RPM external py2-genson 1.0.2
## IMPORT build-with-pip

Requires: python
#%define PipPostBuild \
#   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/lib/python2.7/site-packages/*/*.py
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
