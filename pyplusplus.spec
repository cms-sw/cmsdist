### RPM external pyplusplus 0.8.0
## INITENV +PATH PYTHONPATH %i/lib/python%(echo $PYTHON_VERSION | cut -d. -f 1,2)/site-packages
Source: http://switch.dl.sourceforge.net/sourceforge/pygccxml/%n-%v.tar.gz
Requires: python
%build
%install
python setup.py install --prefix=%i
perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" `grep -r -e "#\!.*python" %i | cut -d: -f1`
