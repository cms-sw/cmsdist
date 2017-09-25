### RPM external py3-pygments 2.1.3
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://pypi.python.org/packages/source/P/Pygments/Pygments-%realversion.tar.gz
Requires: python3 py3-setuptools

%prep
%setup -n Pygments-%realversion

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
for f in %i/bin/pygmentize; do perl -p -i -e 's{.*}{#!/usr/bin/env python3} if $. == 1 && m{#!.*/bin/python}' $f; done
