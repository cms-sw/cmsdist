### RPM external py3-botocore 1.15.49
## IMPORT build-with-pip3

Requires: py3-docutils py3-jmespath py3-python-dateutil py3-urllib3
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
