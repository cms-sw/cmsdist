### RPM external py2-Theano 1.0.1
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}


%define pip_name Theano
Requires: py2-scipy py2-numpy py2-six
## IMPORT build-with-pip

%define PipPostBuild \
   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/theano-nose %{i}/bin/theano-cache %{i}/bin/theano-test
