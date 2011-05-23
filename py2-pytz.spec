### RPM external py2-pytz 2007d 
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://cheeseshop.python.org/packages/source/p/pytz/pytz-%{realversion}.tar.bz2 
Requires: python

%prep
%setup -n pytz-%{realversion}

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
