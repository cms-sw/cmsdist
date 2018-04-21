### RPM external py2-thriftpy 0.3.9
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

BuildRequires: py2-cython

%define pip_name thriftpy

## IMPORT build-with-pip

#%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
