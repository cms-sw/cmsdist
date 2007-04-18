### RPM external py2-sqlalchemy 0.3.5
Requires: gcc-wrapper
%define pythonv %(echo $PYTHON_VERSION | cut -f1,2 -d.)
## INITENV +PATH PYTHONPATH %i/lib/python$(echo $PYTHON_VERSION | cut -f1,2 -d.)/site-packages

Source: http://superb-east.dl.sourceforge.net/sourceforge/sqlalchemy/SQLAlchemy-%v.tar.gz
Requires: python py2-pysqlite  py2-mysqldb py2-cx-oracle

%prep
%setup -n SQLAlchemy-%v
%build
## IMPORT gcc-wrapper
%install
mkdir -p %i/lib/python$(echo $PYTHON_VERSION | cut -f1,2 -d.)/site-packages
python setup.py build
mv build/lib/* %i/lib/python$(echo $PYTHON_VERSION | cut -f1,2 -d.)/site-packages

