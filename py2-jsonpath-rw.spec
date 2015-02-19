### RPM external py2-jsonpath-rw 1.2.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source0: https://pypi.python.org/packages/source/j/jsonpath-rw/jsonpath-rw-%{realversion}.tar.gz
Requires: python py2-six
BuildRequires: py2-setuptools

%prep
%setup -n jsonpath-rw-%{realversion}

%build
python setup.py build

%install
python setup.py install --skip-build --prefix=%{i} --single-version-externally-managed --record=/dev/null

find %i -name '*.egg-info' -exec rm {} \;
# get rid of /usr/bin/python
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'

