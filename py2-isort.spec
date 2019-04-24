### RPM external py2-isort 4.3.17
## IMPORT build-with-pip

Requires: py2-futures py2-backports-functools_lru_cache

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
