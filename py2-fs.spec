### RPM external py2-fs 0.5.5a1
## IMPORT build-with-pip

Requires: py2-six py2-typing
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
