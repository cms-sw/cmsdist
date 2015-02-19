### RPM external py2-httplib2 0.7.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://httplib2.googlecode.com/files/httplib2-%realversion.zip
Requires: python 

%prep
%setup -n httplib2-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
