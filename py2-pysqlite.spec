### RPM external py2-pysqlite 2.8.1
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
Source: https://pypi.python.org/packages/source/p/pysqlite/pysqlite-%realversion.tar.gz
Requires: python sqlite py2-setuptools

%prep
%setup -n pysqlite-%realversion
%build
echo "include_dirs=$SQLITE_ROOT/include" >> setup.cfg
python setup.py build
%install
python setup.py install --prefix=%i
