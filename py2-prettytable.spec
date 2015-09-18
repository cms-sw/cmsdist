### RPM external py2-prettytable 0.7.2
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://prettytable.googlecode.com/files/prettytable-%realversion.tar.gz
Requires: python
BuildRequires: py2-setuptools

%prep
%setup -n prettytable-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -type d -print0 | xargs -0 rm -r --
