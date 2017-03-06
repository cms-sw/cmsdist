### RPM external py2-tqdm 4.11.2
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES


%define pip_name tqdm

## IMPORT build-with-pip

%define PipPostBuild \
   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*

