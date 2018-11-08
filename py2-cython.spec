### RPM external py2-cython 0.29
## IMPORT build-with-pip

%define pip_name Cython
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
