### RPM external py2-marshmallow 1.2.6
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://github.com/marshmallow-code/marshmallow/archive/%realversion.tar.gz
Requires: python
BuildRequires: py2-setuptools

%prep
%setup -n marshmallow-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -type d -print0 | xargs -0 rm -r --
