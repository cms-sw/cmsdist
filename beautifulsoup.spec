### RPM external beautifulsoup 3.1.0.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: http://www.crummy.com/software/BeautifulSoup/download/3.1.x/BeautifulSoup-%{realversion}.tar.gz
Requires: python

%prep
%setup -n BeautifulSoup-%{realversion}

%build
python setup.py build 

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
