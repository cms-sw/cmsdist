### RPM external py2-markupsafe 0.23
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
Source: https://pypi.python.org/packages/source/M/MarkupSafe/MarkupSafe-%realversion.tar.gz
Requires: python py2-setuptools

%prep
%setup -n MarkupSafe-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i  --single-version-externally-managed --record=/dev/null
