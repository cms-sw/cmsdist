### RPM external py3-isort 5.10.1
## IMPORT build-with-pip3

Requires: py3-backports-functools_lru_cache

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
