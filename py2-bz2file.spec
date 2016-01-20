### RPM external py2-bz2file 0.98
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://pypi.python.org/packages/source/b/bz2file/bz2file-%realversion.tar.gz
Requires: python
BuildRequires: py2-setuptools

%prep
%setup -n bz2file-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
