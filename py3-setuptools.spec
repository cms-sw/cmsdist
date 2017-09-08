### RPM external py3-setuptools 18.3.2
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://pypi.python.org/packages/source/s/setuptools/setuptools-%realversion.tar.gz
Requires: python3

%prep
%setup -n setuptools-%realversion

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -exec rm {} \;
rm -f %i/$PYTHON_LIB_SITE_PACKAGES/setuptools/*.exe
for f in %i/bin/easy_install*; do perl -p -i -e 's{.*}{#!/usr/bin/env python3} if $. == 1 && m{#!.*/bin/python}' $f; done
