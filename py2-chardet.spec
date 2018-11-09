### RPM external py2-chardet 3.0.4
## IMPORT build-with-pip

%define PipBuildOptions --upgrade
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
