### RPM external py2-six 1.4.1
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES

%global mod_name six

Source0: https://pypi.python.org/packages/source/s/%{mod_name}/%{mod_name}-%{realversion}.tar.gz
Patch0: py2-six-%{realversion}-use-setuptools

Requires: python py2-setuptools

%prep
%setup -n %{mod_name}-%{realversion}
# we need to patch setup.py to use setuptools instead of distribute
%patch0 -p1

%build
python setup.py build

%install
mkdir -p %{i}/${PYTHON_LIB_SITE_PACKAGES}
export PYTHONPATH=%{i}/${PYTHON_LIB_SITE_PACKAGES}:${PYTHONPATH}

python setup.py install --skip-build --prefix=%{i} --single-version-externally-managed --record=/dev/null 

find %i -name '*.egg-info' -exec rm {} \;
# get rid of /usr/bin/python
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'

