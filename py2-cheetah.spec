### RPM external py2-cheetah 2.4.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: http://pypi.python.org/packages/source/C/Cheetah/Cheetah-%realversion.tar.gz
Requires: python

%prep
%setup -n Cheetah-%realversion
%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
for f in %i/bin/cheetah*; do perl -p -i -e 's{.*}{#!/usr/bin/env python} if $. == 1 && m{#!.*/bin/python}' $f; done
