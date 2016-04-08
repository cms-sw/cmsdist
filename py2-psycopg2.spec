### RPM external py2-psycopg2 2.6.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://initd.org/psycopg/tarballs/PSYCOPG-2-6/psycopg2-%realversion.tar.gz
Requires: python libpq

%prep
%setup -n psycopg2-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
