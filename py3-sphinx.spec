### RPM external py3-sphinx 5.1.1
## IMPORT build-with-pip3

Requires: py3-docutils py3-jinja2 py3-pygments py3-pytz py3-requests py3-imagesize
%define pip_name Sphinx
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
