### RPM external py3-cjson 1.2.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

#Source: http://pypi.python.org/packages/source/p/python-cjson/python-cjson-%{realversion}.tar.gz
Source: https://pypi.python.org/packages/eb/67/ac7744404acd65c96ae342a6585f8070639c3079766c68da56755fb8f029/python-cjson-1.2.1.tar.gz
Requires: python3

%prep
%setup -n python-cjson-%realversion

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
