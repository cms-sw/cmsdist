### RPM external py3-pylint 2.6.0
## IMPORT build-with-pip3

Requires: py3-astroid py3-toml py3-isort py3-mccabe

%define PipPostBuild \
    perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*; \
    perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/lib/python*/site-packages/pylint/test/data/*
