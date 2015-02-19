### RPM external py2-simplejson 1.9.2
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://pypi.python.org/packages/source/s/simplejson/simplejson-%{realversion}.tar.gz
Requires: python
BuildRequires: py2-setuptools

%prep
%setup -n simplejson-%realversion

%build
python setup.py build

%install
# we need simple json only for python 2.5 and earlier, but for python 2.6 and higher
if  [ -z `echo $PYTHON_VERSION | egrep "2.6|3."` ]; then
   python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
   find %i -name '*.egg-info' -exec rm {} \;
fi
