### RPM external py3-stomp 4.1.22
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
#Source: https://pypi.python.org/packages/source/s/stomp.py/stomp.py-%realversion.tar.gz
Source: https://pypi.python.org/packages/d4/ba/3b0248f1c493f5df8dbd67a052f4a6aae6040d39199d032fa9918dc33ebf/stomp.py-%realversion.tar.gz
Requires: python3
BuildRequires: py3-setuptools

%prep
%setup -n stomp.py-%realversion
#perl -p -i -e '/--static-libs/ && s/^(\s+)/$1"") #/' setup.py

%build
python setup.py build

%install
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH \
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
perl -p -i -e 's{^#!.*/python}{#!/usr/bin/env python}' %i/bin/stomp
# Remove documentation.
#%define drop_files %i/share
