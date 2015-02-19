### RPM external py2-sqlalchemy052 0.5.2
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://downloads.sourceforge.net/sqlalchemy/SQLAlchemy-%realversion.tar.gz
Requires: python

%prep
%setup -n SQLAlchemy-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
