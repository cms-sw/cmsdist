### RPM external py2-pycparser 2.19
## IMPORT build-with-pip
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*

