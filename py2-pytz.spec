### RPM external py2-pytz 2014.7
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
Source: https://pypi.python.org/packages/source/p/pytz/pytz-%realversion.tar.gz
Requires: python

%prep
%setup -n pytz-%realversion
%build
%install
python setup.py install --prefix=%i
