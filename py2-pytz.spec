### RPM external py2-pytz 2007d 
Requires: gcc-wrapper
%define pythonv %(echo $PYTHON_VERSION | cut -f1,2 -d.)
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://cheeseshop.python.org/packages/source/p/pytz/pytz-%{v}.tar.bz2 
Requires: python

%prep
%setup -n pytz-%{v}
%build
## IMPORT gcc-wrapper
%install
python setup.py install --prefix=%i
