### RPM external py2-pydoop 1.1.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://pypi.python.org/packages/source/p/pydoop/pydoop-%realversion.tar.gz
Requires: gcc zlib bz2lib openssl python py2-setuptools py2-avro
Provides: libjvm.so()(64bit)

%prep
%setup -n pydoop-%realversion

%build
export JAVA_HOME=/usr/lib/jvm/java
export GCC_ROOT
export PYTHON_ROOT
python setup.py build

%install
export JAVA_HOME=/usr/lib/jvm/java
export GCC_ROOT
export PYTHON_ROOT
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -exec rm {} \;
