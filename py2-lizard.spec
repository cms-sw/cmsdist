### RPM external py2-lizard 1.15.6

%define pip_name lizard 

## IMPORT build-with-pip

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/lizard
