### RPM external py2-pil 1.1.6
## INITENV +PATH PYTHONPATH %i/lib/python$(echo $PYTHON_VERSION | cut -d. -f 1,2)/site-packages
%define downloadn Imaging
Source: http://effbot.org/downloads/%downloadn-%v.tar.gz
Requires: python
# Requires: zlib
# Requires: agg
# Requires: cairo
# py2-numpy is now built using its internal lapack_lite.
# uncomment if otherwise.
# Requires: atlas lapack
Requires: libpng libjpg zlib
# Requires: freetype
%prep
%setup -n %downloadn-%v
perl -p -i -e "s!__PREFIX__!%i!" setup.py

%build
%install
python setup.py install
perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" `grep -r -e "#\!.*python" %i | cut -d: -f1`
