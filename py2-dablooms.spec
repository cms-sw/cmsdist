### RPM external py2-dablooms 0.9.1
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
Source: https://github.com/bitly/dablooms/archive/v%realversion.tar.gz
Requires: python 

%prep
%setup -n dablooms-%realversion

%build
make; cd pydablooms; python setup.py build


%install
cd pydablooms; python setup.py install --prefix=%i
