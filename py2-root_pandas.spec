### RPM external py2-root_pandas 0.3.1
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}

BuildRequires: py2-numpy py2-pandas py2-root_numpy

%define pip_name root_pandas

## IMPORT build-with-pip

#%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
