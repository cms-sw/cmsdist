### RPM external py2-tempora 1.14.1
## IMPORT build-with-pip
Requires: py2-six py2-pytz py2-jaraco-functools

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
