### RPM external py2-jinja 2.5.2
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://pypi.python.org/packages/source/J/Jinja2/Jinja2-%realversion.tar.gz
Requires: python py2-setuptools

%prep
%setup -n Jinja2-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
