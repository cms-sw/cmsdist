### RPM external py2-pygments 1.6
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES

Source: http://pypi.python.org/packages/source/P/Pygments/Pygments-%realversion.tar.gz
Requires: python py2-setuptools

%prep
%setup -n Pygments-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
