### RPM external cmsmonitoring 0.3.1
## IMPORT build-with-pip

Requires: python py2-stomp py2-jsonschema py2-genson py2-tornado py2-nats

#%define PipPostBuild \
#   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/lib/python2.7/site-packages/*/*.py
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
