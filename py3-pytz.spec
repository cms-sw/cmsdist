### RPM external py3-pytz 2016.10
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

#Source: http://cheeseshop.python.org/packages/source/p/pytz/pytz-%{realversion}.tar.bz2 
Source: https://pypi.python.org/packages/42/00/5c89fc6c9b305df84def61863528e899e9dccb196f8438f6cbe960758fc5/pytz-%{realversion}.tar.gz
Requires: python3

%prep
%setup -n pytz-%{realversion}

%build
python3 setup.py build

%install
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH \
python3 setup.py install --prefix=%i
