### RPM external py2-sympy 0.7.6
## INITENV +PATH PYTHONPATH %i/lib/python$(echo $PYTHON_VERSION | cut -d. -f 1,2)/site-packages
Source: http://service-spi.web.cern.ch/service-spi/external/tarFiles/sympy-%{realversion}.tar.gz
Requires: python
%prep
%setup -n sympy-%{realversion}

%build
python setup.py build

%install
python setup.py	install --prefix=%{i}

perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" `grep -r -e "#\!.*python" %i | cut -d: -f1`
