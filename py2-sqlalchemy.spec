### RPM external py2-sqlalchemy 0.8.2
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES

Source: https://pypi.python.org/packages/source/S/SQLAlchemy/SQLAlchemy-%{realversion}.tar.gz
Requires: python 

%prep
%setup -n SQLAlchemy-%{realversion}

%build
python setup.py build

%install
python setup.py install --skip-build --prefix=%{i}

find %{i} -name '*.egg-info' -exec rm {} \;
