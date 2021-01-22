### RPM external python-ldap 2.4.10
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://pypi.python.org/packages/source/p/%n/%n-%{realversion}.tar.gz
Requires: python openldap

%prep
%setup -q -n %n-%{realversion}

%build
perl -p -i -e "s:(library_dirs =)(.*):\1 ${PYTHON_ROOT}/lib ${OPENLDAP_ROOT}/lib:g" setup.cfg
perl -p -i -e "s:(include_dirs =)(.*):\1 ${PYTHON_ROOT}/include ${OPENLDAP_ROOT}/include:g" setup.cfg
perl -p -i -e "s:(defines = )(.*):\1 HAVE_TLS HAVE_LIBLDAP_R:g" setup.cfg
# to avoid a UnicodeDecodeError exception
perl -p -i -e "s/Michael Ströder/Michael Stroder/g" setup.cfg
python setup.py build

%install
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH \
python setup.py install --prefix=%i 
find %i -name '*.egg-info' -exec rm {} \;
perl -p -i -e 's{^#!.*/python}{#!/usr/bin/env python}' %i/bin/*
