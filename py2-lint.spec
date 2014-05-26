### RPM external py2-lint 0.25.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source0: http://download.logilab.org/pub/common/logilab-common-0.57.1.tar.gz
Source1: http://download.logilab.org/pub/astng/logilab-astng-0.23.1.tar.gz
Source2: http://download.logilab.org/pub/pylint/pylint-%{realversion}.tar.gz
Requires: python

%prep
%setup -T -b 0 -n logilab-common-0.57.1
%setup -D -T -b 1 -n logilab-astng-0.23.1
%setup -D -T -b 2 -n pylint-%{realversion}

%build
for d in ../logilab-common-* ../logilab-astng-* ../pylint-*; do
  cd $d
  python setup.py build
done

%install
for d in ../logilab-common-* ../logilab-astng-* ../pylint-*; do
  cd $d
  python setup.py install --prefix=%i
done
find %i -name '*.egg-info' -exec rm {} \;
perl -p -i -e 's{^#!.*/python}{#!/usr/bin/env python}' %i/bin/*
