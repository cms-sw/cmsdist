### RPM external py3-pycurl 7.19.3
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: http://pycurl.sourceforge.net/download/pycurl-%realversion.tar.gz
Requires: openssl python3 curl

%prep
%setup -n pycurl-%realversion
perl -p -i -e 's/,\s+"--static-libs"]/]/' setup.py

%build
export CPPFLAGS="-I ${OPENSSL_ROOT}/include $CPPFLAGS"
export PYTHON3_ROOT
export LDFLAGS="-L$PYTHON3_ROOT/lib $LDFLAGS"
python3 setup.py build --with-ssl

%install
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH \
python3 setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
# Remove documentation.
%define drop_files %i/share
