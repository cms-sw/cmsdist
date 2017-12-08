### RPM external py2-pandas 0.21.0
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}

%define pip_name pandas
Requires: py2-six py2-python-dateutil py2-pytz py2-numpy 

## IMPORT build-with-pip
#%define PipPostBuild \
#perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" `grep -r -e "#\!.*python" %i | cut -d: -f1`
