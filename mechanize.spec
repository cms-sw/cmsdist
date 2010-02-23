### RPM external mechanize 0.1.11
%define pythonv `echo $PYTHON_VERSION |cut -d. -f1,2`
## INITENV +PATH PYTHONPATH %i/lib/python%{pythonv}/site-packages

# this is where mechanize version 0.1.11 is located
# changed ez_setup to use version 0.6c11
Source: http://cern.ch/giffels/mechanize-%realversion.tar.gz
Requires: python

%prep
%setup -n mechanize-%realversion
%build
python setup.py build
%install
export PYTHONPATH=$PYTHONPATH:%i/lib/python%{pythonv}/site-packages/
mkdir -p %i/lib/python%{pythonv}/site-packages/
python setup.py install --prefix=%i

# The following may be needed if your python files are using full paths
# to the interpreter instead of /usr/bin/env python
perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" `grep -r -e "^#\!.*python.*" %i | cut -d: -f1`
