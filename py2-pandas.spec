### RPM external py2-pandas 0.15.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: https://pypi.python.org/packages/source/p/pandas/pandas-%realversion.tar.gz
Requires: python py2-numpy py2-python-dateutil py2-setuptools

%prep
%setup -n pandas-%realversion

%build
%install
case %cmsos in
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac

mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH \
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
find %i/$PYTHON_LIB_SITE_PACKAGES -name '*.py' -exec chmod a-x {} \;
perl -p -i -e 's{^#!.*/python}{#!/usr/bin/env python}' %i/bin/*
