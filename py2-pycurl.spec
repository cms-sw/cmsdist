### RPM external py2-pycurl 7.19.3.1
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
Source: http://pycurl.sourceforge.net/download/pycurl-%realversion.tar.gz
Requires: python curl

%prep
%setup -n pycurl-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
# Remove documentation.
%define drop_files %i/share
