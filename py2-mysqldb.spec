### RPM external py2-mysqldb 1.2.0
%define pythonv $(echo $PYTHON_VERSION | cut -d. -f 1,2)
## INITENV +PATH PYTHONPATH %i/lib/python%{pythonv}/site-packages
%define downloadn MySQL-python
Source: http://belnet.dl.sourceforge.net/sourceforge/mysql-python/%downloadn-%v.tar.gz
Requires: python mysql 
%prep
%setup -n %downloadn-%v
%build
python setup.py build
%install
python setup.py install --prefix=%{i}
