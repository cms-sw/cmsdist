### RPM external py3-cheroot 8.2.1
## IMPORT build-with-pip3
Requires: py3-backports-functools_lru_cache py3-six py3-more-itertools py3-jaraco-functools

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
