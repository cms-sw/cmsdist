### RPM external py3-cjson 1.0.5
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://pypi.python.org/packages/source/p/python-cjson/python-cjson-%{realversion}.tar.gz
Requires: python3

%prep
%setup -n python-cjson-%realversion

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
