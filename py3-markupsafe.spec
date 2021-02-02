### RPM external py3-markupsafe 1.1.1
## IMPORT build-with-pip3
%define pip_name MarkupSafe
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
