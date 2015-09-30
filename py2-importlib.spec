### RPM external py2-importlib 1.0.3
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: https://pypi.python.org/packages/source/i/importlib/importlib-%realversion.tar.gz
Requires: python
BuildRequires: py2-setuptools

%prep
%setup -n importlib-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --record=/dev/null

# Don't delete egg-info since the futurize script need it to load the future library
#find %i -name '*.egg-info' -print0 | xargs -0 rm -rf --
