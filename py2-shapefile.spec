### RPM external py2-shapefile 1.1.4
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: svn://pyshp.googlecode.com/svn/trunk@78?scheme=http&strategy=export&module=pyshp&output=/pyshp.tar.gz
Requires: python

%prep
%setup -n pyshp

%build

%install
# The setup.py uses py2-setuptools which just makes a mess of the
# one .py file in pyshp. So do the installation manually.
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
cp shapefile.py %i/$PYTHON_LIB_SITE_PACKAGES
python -m compileall %i/$PYTHON_LIB_SITE_PACKAGES
