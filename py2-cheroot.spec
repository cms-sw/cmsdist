### RPM external py2-cheroot 6.5.5
## IMPORT build-with-pip
Requires: py2-backports-functools_lru_cache py2-six py2-more-itertools 

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
