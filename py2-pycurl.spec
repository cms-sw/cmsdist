### RPM external py2-pycurl 7.43.0
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES
Source: https://dl.bintray.com/pycurl/pycurl/pycurl-%{realversion}.tar.gz
Requires: python curl openssl

%prep
%setup -n pycurl-%{realversion}

%build
python setup.py --with-openssl build

%install
python setup.py --with-openssl install --prefix=%{i}
find %{i}/${PYTHON_LIB_SITE_PACKAGES} -name '*.egg-info' -print0 | xargs -0 rm -rf
rm -rf %{i}/share
