### RPM external py2-gitpython 1.0.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://pypi.python.org/packages/source/G/GitPython/GitPython-%realversion.tar.gz
Requires: python py2-gitdb
BuildRequires: py2-setuptools

%prep
%setup -n GitPython-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -type d -print0 | xargs -0 rm -r --
