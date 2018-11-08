### RPM external py2-ipython 5.8.0
## IMPORT build-with-pip

Requires: py2-traitlets py2-pickleshare py2-Pygments py2-prompt_toolkit py2-pexpect py2-simplegeneric py2-backports
%define PipPostBuild \
    perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*; \
    perl -p -i -e "s|^#!.*python3|#!/usr/bin/env python3|" %{i}/bin/*
