### RPM external py2-mysqldb 1.2.3c1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
%define downloadn MySQL-python
Source: http://heanet.dl.sourceforge.net/sourceforge/mysql-python/%downloadn-%realversion.tar.gz
Requires: python mysql 
Patch0: py2-mysqldb-setup

%prep
%setup -n %downloadn-%realversion
%patch0 -p0

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
