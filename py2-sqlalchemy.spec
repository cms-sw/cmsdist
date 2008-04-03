### RPM external py2-sqlalchemy 0.4.4
%define pythonv %(echo $PYTHON_VERSION | cut -f1,2 -d.)
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://superb-east.dl.sourceforge.net/sourceforge/sqlalchemy/SQLAlchemy-%realversion.tar.gz
Requires: python py2-mysqldb py2-cx-oracle py2-pysqlite
#Patch: py2-sqlalchemy-setup
%prep
%setup -n SQLAlchemy-%realversion
%patch0 -p1
%build
%install
mkdir -p %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages
python setup.py build
mv build/lib/* %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages


