### RPM external pysqlite 2.3.1
%define pythonv %(echo $PYTHON_VERSION | cut -f1,2 -d.)
## INITENV +PATH PYTHONPATH %i/lib/python%{pythonv}/site-packages
Source: http://initd.org/pub/software/pysqlite/releases/2.3/%v/%n-%v.tar.gz
Requires: python sqlite

%build
python setup.py build
%install
python setup.py install --prefix=%i
