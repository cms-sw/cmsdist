### RPM external py3-pylint 1.9.4
## IMPORT build-with-pip3

Requires: py3-astroid py3-backports-functools_lru_cache py3-configparser py3-isort py3-mccabe py3-singledispatch py3-six

%define PipPostBuild \
    perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*; \
    perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/lib/python*/site-packages/pylint/test/data/*
