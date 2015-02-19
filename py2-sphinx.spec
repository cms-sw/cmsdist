### RPM external py2-sphinx 1.1.3
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://pypi.python.org/packages/source/S/Sphinx/Sphinx-%realversion.tar.gz
Requires: python py2-docutils py2-jinja py2-pygments py2-setuptools

%prep
%setup -n Sphinx-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
for f in %i/bin/sphinx-*; do perl -p -i -e 's{.*}{#!/usr/bin/env python} if $. == 1 && m{#!.*/bin/python}' $f; done
