### RPM external py3-cmsmonitoring 0.6.9
## IMPORT build-with-pip3

%define pip_name cmsmonitoring
Requires: py3-stomp py3-jsonschema py3-genson

# Relax dependency on jsonschema to avoid incompatibilities with rucio-clients
%define PipPreBuild perl -p -i -e "s|^jsonschema>=4|jsonschema>=3.2|" %{i}/src/*

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
