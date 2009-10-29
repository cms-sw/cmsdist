### RPM external mechanize 0.1.11
%define pythonv `echo $PYTHON_VERSION |cut -d. -f1,2`
## INITENV +PATH PYTHONPATH %i/lib/python%{pythonv}/site-packages

# this is where mechanize version 0.1.11 is located
Source: http://wwwsearch.sourceforge.net/mechanize/src/mechanize-%realversion.tar.gz
Requires: python

%prep
%setup -n mechanize-%realversion
%build
python setup.py build
%install
export PYTHONPATH=$PYTHONPATH:%i/lib/python%{pythonv}/site-packages/
mkdir -p %i/lib/python%{pythonv}/site-packages/
python setup.py install --prefix=%i
