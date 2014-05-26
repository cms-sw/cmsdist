### RPM external py2-mongoengine 0.3
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://github.com/hmarr/mongoengine/tarball/v0.3
Requires: python
BuildRequires: py2-sphinx py2-setuptools

%prep
%setup -n hmarr-mongoengine-d314d88

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -exec rm {} \;
