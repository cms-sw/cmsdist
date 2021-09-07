### RPM external py3-pygments 2.10.0
## IMPORT build-with-pip3

%define pip_name Pygments
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
