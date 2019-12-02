### RPM external py3-cmsmonitoring 0.2.4
## IMPORT build-with-pip3

%define pip_name cmsmonitoring
Requires: python3 py3-stomp py3-jsonschema py3-genson

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
