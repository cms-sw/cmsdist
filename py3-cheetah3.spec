### RPM external py3-cheetah3 3.2.6.post2
## IMPORT build-with-pip3

Requires: py3-markdown
%define pip_name Cheetah3

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
