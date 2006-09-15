### RPM external py2-matplotlib 0.87.4
## INITENV +PATH PYTHONPATH %i/lib/python%(echo $PYTHON_VERSION | cut -d. -f 1,2)/site-packages
%define downloadn matplotlib
Source: http://switch.dl.sourceforge.net/sourceforge/%downloadn/%downloadn-%v.tar.gz
Requires: python
Requires: zlib
# Requires: agg
# Requires: cairo
Requires: py2-numpy
Requires: libpng
# Requires: freetype
%prep
%setup -n %downloadn-%v

%build
%install
python setup.py install --prefix=%i
perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" `grep -r -e "#\!.*python" %i | cut -d: -f1`
