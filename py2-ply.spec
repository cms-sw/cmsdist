### RPM external py2-ply 3.4
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://www.dabeaz.com/ply/ply-%realversion.tar.gz
Requires: python

%prep
%setup -n ply-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
