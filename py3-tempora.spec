### RPM external py3-tempora 1.14.1
## IMPORT build-with-pip3
Requires: py3-six py3-pytz py3-jaraco-functools

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
