### RPM external py2-psutil 0.6.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://psutil.googlecode.com/files/psutil-%realversion.tar.gz
Requires: python 

%prep
%setup -n psutil-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
find %i -name '.package-checksum' -exec rm {} \;
