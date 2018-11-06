### RPM external py2-flake8 3.5.0
## IMPORT build-with-pip

Requires: py2-backports py2-enum34 py2-mccabe py2-pycodestyle py2-pyflakes
BuildRequires: py2-configparser
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
