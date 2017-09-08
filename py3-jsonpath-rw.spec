### RPM external py3-jsonpath-rw 1.2.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source0: https://pypi.python.org/packages/source/j/jsonpath-rw/jsonpath-rw-%{realversion}.tar.gz
Requires: python3 py3-six
BuildRequires: py3-setuptools

%prep
%setup -n jsonpath-rw-%{realversion}

%build
python3 setup.py build

%install
python3 setup.py install --skip-build --prefix=%{i} --single-version-externally-managed --record=/dev/null

find %i -name '*.egg-info' -exec rm {} \;
# get rid of /usr/bin/python
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python3}'

