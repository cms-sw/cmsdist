### RPM external py2-cx-oracle 4.2
%define pythonv `echo $PYTHON_VERSION |cut -d. -f1,2`
## INITENV +PATH PYTHONPATH %i/lib/python%{pythonv}/site-packages
%define downloadn cx_Oracle
Source: http://switch.dl.sourceforge.net/sourceforge/cx-oracle/%downloadn-%realversion.tar.gz
Requires: python
Requires: oracle
%prep
%setup -n %downloadn-%realversion

%build
%install
perl -p -i -e 's/(?<=includeDirs = \[)/"include", /' setup.py
python setup.py install --prefix=%i
