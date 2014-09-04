### RPM external py2-pyparsing 2.0.2
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://pypi.python.org/packages/source/p/pyparsing/pyparsing-%realversion.tar.gz
Requires: python

%prep
%setup -n pyparsing-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
