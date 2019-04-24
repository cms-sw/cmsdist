### RPM external py2-pylint 1.9.4
## IMPORT build-with-pip

Requires: py2-astroid py2-backports-functools_lru_cache py2-configparser py2-isort py2-mccabe py2-singledispatch py2-six

%define PipPostBuild \
    perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*; \
    perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/lib/python*/site-packages/pylint/test/data/*
