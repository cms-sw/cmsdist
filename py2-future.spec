### RPM external py2-future 0.18.2
## IMPORT build-with-pip

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
