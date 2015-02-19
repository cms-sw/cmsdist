### RPM external py2-whoosh 2.4.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source0: https://pypi.python.org/packages/source/W/Whoosh/Whoosh-%{realversion}.tar.gz

Requires: python
BuildRequires: py2-sphinx py2-setuptools

%prep
%setup -n Whoosh-%{realversion}

%build
python setup.py build

%install
python setup.py install -O1 --skip-build --prefix=%{i} --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -exec rm {} \;
# get rid of /usr/bin/python
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'

