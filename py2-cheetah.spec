### RPM external py2-cheetah 2.4.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: http://pypi.python.org/packages/source/C/Cheetah/Cheetah-%realversion.tar.gz
Requires: python py2-markdown

%prep
%setup -n Cheetah-%realversion
%build
python setup.py build

%install
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH \
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/lib/python2.7/site-packages/Cheetah-2.4.0-py2.7-linux-x86_64.egg/EGG-INFO/scripts/*
