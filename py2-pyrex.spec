### RPM external py2-pyrex 0.9.9
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://www.cosc.canterbury.ac.nz/greg.ewing/python/Pyrex/Pyrex-%realversion.tar.gz
Requires: python

%prep
%setup -n Pyrex-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
for f in %i/bin/pyrexc; do perl -p -i -e 's{.*}{#!/usr/bin/env python} if $. == 1 && m{#!.*/bin/python}' $f; done
