### RPM external py2-sqlalchemy 1.1.4
## INITENV +PATH PYTHON27PATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://pypi.python.org/packages/ca/ca/c2436fdb7bb75d772d9fa17ba60c4cfded6284eed053a7274b2beb96596a/SQLAlchemy-%{realversion}.tar.gz
Requires: python py2-setuptools

#%define pythonver %(echo %{allpkgreqs} | tr ' ' '\\n' | grep ^external/python/ | cut -d/ -f3 | cut -d. -f 1,2)
#%define pyArch %(uname -m)


Patch0: py2-sqlalchemy-1.1.4-add-frontier-dialect
Patch1: py2-sqlalchemy-1.1.4-fix-sqlite-dialect-timestamp

%prep
%setup -n SQLAlchemy-%{realversion}
%patch0 -p1
%patch1 -p1

%build
python setup.py build

%install
mkdir -p %{i}/${PYTHON_LIB_SITE_PACKAGES}
PYTHONPATH=%{i}/${PYTHON_LIB_SITE_PACKAGES}:${PYTHONPATH} python setup.py install --skip-build --prefix=%{i}

