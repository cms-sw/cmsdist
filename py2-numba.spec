### RPM external py2-numba 0.39.0
## IMPORT build-with-pip

Requires: py2-funcsigs py2-enum34 py2-six py2-singledispatch py2-llvmlite py2-numpy
%define source0 git+https://github.com/numba/numba?obj=master/9ed665ea67ce293b94c641aab0387fc846588b38&export=numba-%{realversion}&output=/source.tar.gz
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
