### RPM external py2-cx-oracle 5.0.1
%define pythonv `echo $PYTHON_VERSION |cut -d. -f1,2`
## INITENV +PATH PYTHONPATH %i/lib/python%{pythonv}/site-packages
%define downloadn cx_Oracle
Source: http://switch.dl.sourceforge.net/sourceforge/cx-oracle/%downloadn-%realversion.tar.gz
Requires: python oracle oracle-env
%prep
%setup -n %downloadn-%realversion

%build
%install
perl -p -i -e 's/(?<=includeDirs = \[)/"include", userOracleHome+"\/include" /' setup.py
python setup.py install --prefix=%i
