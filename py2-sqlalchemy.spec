### RPM external py2-sqlalchemy 1.1.4
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES

Source: https://pypi.python.org/packages/ca/ca/c2436fdb7bb75d772d9fa17ba60c4cfded6284eed053a7274b2beb96596a/SQLAlchemy-%{realversion}.tar.gz
Requires: python 

# re-use the patches for the previous version...
Patch0: py2-sqlalchemy-0.8.2-add-frontier-dialect
Patch1: py2-sqlalchemy-0.8.2-fix-sqlite-dialect-timestamp

%prep
%setup -n SQLAlchemy-%{realversion}
%patch0 -p1
%patch1 -p1

%build
python setup.py build

%install
python setup.py install --skip-build --prefix=%{i}

find %{i} -name '*.egg-info' -exec rm {} \;
