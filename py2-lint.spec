### RPM external py2-lint 1.3.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source0: https://pypi.python.org/packages/source/l/logilab-common/logilab-common-0.63.2.tar.gz
Source1: https://bitbucket.org/logilab/astroid/get/astroid-1.2.1.tar.gz
Source2: https://pypi.python.org/packages/source/p/pylint/pylint-%{realversion}.zip
Requires: python
BuildRequires: py2-setuptools

%prep
%setup -T -b 0 -n logilab-common-0.63.2
%setup -D -T -b 1 -n logilab-astroid-315668c10333
%setup -D -T -b 2 -n pylint-%{realversion}

%build
for d in ../logilab-common-* ../logilab-astroid-* ../pylint-*; do
  cd $d
  python setup.py build
done

%install
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH
for d in ../logilab-common-* ../logilab-astroid-* ../pylint-*; do
  cd $d
  python setup.py install --prefix=%i
done
find %i -name '*.egg-info' -exec rm {} \;
perl -p -i -e 's{^#!.*/python}{#!/usr/bin/env python}' %i/bin/*