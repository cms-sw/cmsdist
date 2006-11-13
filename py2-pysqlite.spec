### RPM external py2-pysqlite 2.3.2
%define pythonv %(echo $PYTHON_VERSION | cut -f1,2 -d.)
%define distname pysqlite-%v
## INITENV +PATH PYTHONPATH %i/lib/python%{pythonv}/site-packages
Source: http://initd.org/pub/software/pysqlite/releases/2.3/%v/%{distname}.tar.gz
Requires: python sqlite

%prep
%setup -n %{distname}
%build
perl -p -i -e "s!include_dirs=.*!include_dirs=$SQLITE_ROOT/include!" setup.cfg
perl -p -i -e "s!library_dirs=.*!library_dirs=$SQLITE_ROOT/lib!" setup.cfg
python setup.py build
%install
python setup.py install --prefix=%i
