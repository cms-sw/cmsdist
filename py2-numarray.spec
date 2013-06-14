### RPM external py2-numarray 1.5.2
## INITENV +PATH PYTHONPATH %i/lib/python$(echo $PYTHON_VERSION | cut -d. -f 1,2)/site-packages
%define downloadn numarray
Source: http://switch.dl.sourceforge.net/sourceforge/numpy/%downloadn-%v.tar.gz
Requires: python
%prep
%setup -n %downloadn-%v

%build
%install
python setup.py install --prefix=%i
perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" `grep -r -e "#\!.*python" %i | cut -d: -f1`
