### RPM external cmsmonitoring 0.2.1
## IMPORT build-with-pip

Requires: python py2-stomp py2-jsonschema py2-genson

#%define PipPostBuild \
#   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/lib/python2.7/site-packages/*/*.py
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
