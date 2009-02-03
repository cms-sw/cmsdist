### RPM external py2-memcached 1.43
%define pythonv %(echo $PYTHON_VERSION | cut -f1,2 -d.)
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: ftp://ftp.tummy.com/pub/python-memcached/old-releases/python-memcached-%realversion.tar.gz
Requires: python py2-setuptools
%prep
%setup -n python-memcached-%realversion
%build
%install
mkdir -p %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages
python setup.py build
mv build/lib/* %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages


