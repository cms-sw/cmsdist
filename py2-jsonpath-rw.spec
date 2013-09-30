### RPM external py2-jsonpath-rw 1.2.0
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES

%global mod_name jsonpath-rw

Source0: https://pypi.python.org/packages/source/j/%{mod_name}/%{mod_name}-%{realversion}.tar.gz

Requires: python py2-setuptools

%prep
%setup -n %{mod_name}-%{realversion}

%build
python setup.py build

%install
mkdir -p %{i}/${PYTHON_LIB_SITE_PACKAGES}
export PYTHONPATH=%{i}/${PYTHON_LIB_SITE_PACKAGES}:${PYTHONPATH}

python setup.py install --skip-build --prefix=%{i} --single-version-externally-managed --record=/dev/null 

find %i -name '*.egg-info' -exec rm {} \;
# get rid of /usr/bin/python
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'

