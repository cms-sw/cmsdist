### RPM external py2-docutils 0.7
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES

Source: http://downloads.sourceforge.net/docutils/docutils-%{realversion}.tar.gz
Requires: python

%prep
%setup -n docutils-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i
for f in %i/bin/rst*; do perl -p -i -e 's{.*}{#!/usr/bin/env python} if $. == 1 && m{#!.*/bin/python}' $f; done
