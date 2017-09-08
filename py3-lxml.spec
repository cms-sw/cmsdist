### RPM external py3-lxml 3.7.2
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

#Source: http://codespeak.net/lxml/lxml-%{realversion}.tgz
Source: https://pypi.python.org/packages/66/45/f11fc376f784c6f2e77ffc7a9d02374ff3ceb07ede8c56f918939409577c/lxml-%{realversion}.tar.gz
Requires: python3 libxml2 libxslt zlib

%prep
%setup -n lxml-%realversion

%build
export PYTHON3_ROOT
export LDFLAGS="-L$PYTHON3_ROOT/lib $LDFLAGS"
export LDFLAGS="-L $ZLIB_ROOT/lib $LDFLAGS"
python3 setup.py build

%install
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH \
python3 setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
