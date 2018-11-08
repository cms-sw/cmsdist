### RPM external py2-Theano 1.0.2
## IMPORT build-with-pip

Requires: py2-scipy py2-six
%define PipPostBuild \
   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/theano-nose %{i}/bin/theano-cache %{i}/bin/theano-test
