### RPM external py2-future 0.16.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

## IMPORT build-with-pip

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
