### RPM external py2-lint 2.2.3
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
%define logilab_ver 1.4.2
%define astroid_ver 1.6.6
Source0: https://pypi.python.org/packages/source/l/logilab-common/logilab-common-%{logilab_ver}.tar.gz
Source1: https://pypi.python.org/packages/source/a/astroid/astroid-%{astroid_ver}.tar.gz
Source2: https://pypi.python.org/packages/source/p/pylint/pylint-%realversion.tar.gz
Requires: python
BuildRequires: py2-setuptools

%prep
%setup -T -b 0 -n logilab-common-%{logilab_ver}
%setup -D -T -b 1 -n astroid-%{astroid_ver}
%setup -D -T -b 2 -n pylint-%{realversion}

%build
for d in ../logilab-common-* ../astroid-* ../pylint-*; do
  cd $d
  python setup.py build
done

%install
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH
for d in ../logilab-common-* ../astroid-* ../pylint-*; do
  cd $d
  python setup.py install --prefix=%i
done
find %i -name '*.egg-info' -exec rm {} \;
perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/* \
                                                     %{i}/lib/python*/site-packages/pylint-*.egg/EGG-INFO/scripts/* \
                                                     %{i}/lib/python*/site-packages/pylint-*.egg/pylint/test/data/* \
                                                     %{i}/lib/python*/site-packages/logilab_common-*.egg/EGG-INFO/scripts/*
