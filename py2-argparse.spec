### RPM external py2-argparse 1.3.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://pypi.python.org/packages/source/a/argparse/argparse-%realversion.tar.gz
Requires: python
BuildRequires: py2-setuptools

%prep
%setup -n argparse-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -type d -print0 | xargs -0 rm -r --
