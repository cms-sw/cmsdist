### RPM external py2-mysqldb 1.2.4b4
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
%define downloadn MySQL-python

Source: https://pypi.python.org/packages/source/M/MySQL-python/%downloadn-%realversion.tar.gz
Requires: python mariadb
Patch0: py2-mysqldb-setup

%prep
%setup -n %downloadn-%realversion
%patch0 -p0

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
