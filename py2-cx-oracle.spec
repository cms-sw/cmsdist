### RPM external py2-cx-oracle 4.2
## BUILDIF case $(uname):$(uname -p) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac
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
