### RPM external py2-six 1.4.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source0: https://pypi.python.org/packages/source/s/six/six-%{realversion}.tar.gz
Requires: python

%prep
%setup -n six-%{realversion}

%build
python setup.py build

%install
python setup.py install --skip-build --prefix=%{i}
find %i -name '*.egg-info' -exec rm {} \;
# get rid of /usr/bin/python
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'

