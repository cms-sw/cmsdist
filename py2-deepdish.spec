### RPM external py2-deepdish 0.3.4
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES


%define pip_name deepdish
Requires: py2-tables py2-six py2-scipy py2-numexpr py2-numpy 

## IMPORT build-with-pip

%define PipPostBuild \
   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/ddls
