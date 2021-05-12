### RPM external py3-cmscouchapp 1.3.0
## IMPORT build-with-pip3

%define pip_name CMSCouchapp

Requires: py3-requests
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
