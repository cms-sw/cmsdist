### RPM external py2-pystemmer 1.0.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://snowball.tartarus.org/wrappers/PyStemmer-%{realversion}.tar.gz
Requires: python 

%prep
%setup -n PyStemmer-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
