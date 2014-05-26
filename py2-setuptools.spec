### RPM external py2-setuptools 0.6c9
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://pypi.python.org/packages/source/s/setuptools/setuptools-%realversion.tar.gz
Requires: python

%prep
%setup -n setuptools-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -exec rm {} \;
rm -f %i/$PYTHON_LIB_SITE_PACKAGES/setuptools/*.exe
for f in %i/bin/easy_install*; do perl -p -i -e 's{.*}{#!/usr/bin/env python} if $. == 1 && m{#!.*/bin/python}' $f; done
