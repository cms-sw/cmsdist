### RPM external py3-whoosh 2.7.4
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source0: https://pypi.python.org/packages/source/W/Whoosh/Whoosh-%{realversion}.tar.gz

Requires: python3
BuildRequires: py3-sphinx py3-setuptools

%prep
%setup -n Whoosh-%{realversion}

%build
python3 setup.py build

%install
python3 setup.py install -O1 --skip-build --prefix=%{i} --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -exec rm {} \;
# get rid of /usr/bin/python
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python3}'

