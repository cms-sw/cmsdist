### RPM external py3-pylint 2.14.5
## IMPORT build-with-pip3

Requires: py3-astroid py3-toml py3-isort py3-mccabe py3-dill py3-platformdirs py3-tomli py3-tomlkit

%define PipPostBuild \
    perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*; \
    perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/lib/python*/site-packages/pylint/test/data/*
