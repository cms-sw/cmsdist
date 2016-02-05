### RPM external py2-avro 1.7.7
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://pypi.python.org/packages/source/a/avro/avro-%realversion.tar.gz
Requires: python
BuildRequires: py2-setuptools

%prep
%setup -n avro-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -exec rm {} \;
