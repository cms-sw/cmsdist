### RPM external py2-cx-oracle 4.2
## INITENV +PATH PYTHONPATH %i/lib/python$(echo $PYTHON_VERSION | cut -d. -f 1,2)/site-packages
%define downloadn cx_Oracle
Source: http://switch.dl.sourceforge.net/sourceforge/cx-oracle/%downloadn-%v.tar.gz
Requires: python
Requires: oracle
%prep
%setup -n %downloadn-%v

%build
%install
perl -p -i -e 's/(?<=includeDirs = \[)/"include", /' setup.py
python setup.py install --prefix=%i
