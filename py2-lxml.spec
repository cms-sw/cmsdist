### RPM external py2-lxml 2.2.6
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://codespeak.net/lxml/lxml-%{realversion}.tgz
Requires: python libxml2 libxslt

%prep
%setup -n lxml-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
