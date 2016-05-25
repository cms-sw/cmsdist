### RPM external py2-pytest 2.9.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: http://pypi.python.org/packages/source/p/pytest/pytest-%{realversion}.tar.gz
Requires: python py2-setuptools py2-py

%prep
%setup -n pytest-%{realversion}

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -exec rm {} \;
