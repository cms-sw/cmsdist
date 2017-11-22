### RPM external python-ldap 2.5.2
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}

Source: https://pypi.python.org/packages/3f/97/b8482a7c57cf20f9b1a89085cd634dbba6eb7f34bb18e0206820266fb8e1/python-ldap-2.5.2.tar.gz
Requires: python openssl openldap

%prep
%setup -q -n %{n}-%{realversion}

%build
sed -i'' "s:\(library_dirs =\)\(.*\):\1 ${OPENSSL_ROOT}\/lib ${PYTHON_ROOT}\/lib ${OPENLDAP_ROOT}\/lib:g" setup.cfg
sed -i'' "s:\(include_dirs =\)\(.*\):\1 ${OPENSSL_ROOT}\/include ${PYTHON_ROOT}\/include ${OPENLDAP_ROOT}\/include:g" setup.cfg
sed -i'' "s:\(defines = \)\(.*\):\1 HAVE_TLS HAVE_LIBLDAP_R:g" setup.cfg

python setup.py build

%install

mkdir -p %{i}/${PYTHON_LIB_SITE_PACKAGES}
export PYTHONPATH=%{i}/${PYTHON_LIB_SITE_PACKAGES}:${PYTHONPATH}

python setup.py install --skip-build --prefix=%{i}
