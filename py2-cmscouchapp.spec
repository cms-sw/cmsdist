### RPM external py2-cmscouchapp 1.2.10
## IMPORT build-with-pip

%define pip_name CMSCouchapp

Requires: py2-requests
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
