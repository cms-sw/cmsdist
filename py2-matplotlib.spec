### RPM external py2-matplotlib 0.90.1
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
%define downloadn matplotlib
Source: http://switch.dl.sourceforge.net/sourceforge/%downloadn/%downloadn-%v.tar.gz
Requires: python
Requires: zlib
# Requires: agg
# Requires: cairo
Requires: py2-numpy 
# py2-numpy is now built using its internal lapack_lite.
# uncomment if otherwise.
# Requires: atlas lapack
Requires: libpng
# Requires: freetype
Patch0: matplotlib-0.90.1
%prep
%setup -n %downloadn-%v
%patch0 -p0
perl -p -i -e "s|\@LIBPNG_ROOT\@|$LIBPNG_ROOT|;s|\@ZLIB_ROOT\@|$ZLIB_ROOT|" setupext.py
%build
%install
python -c 'import numpy'
python setup.py install --prefix=%i
perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" `grep -r -e "#\!.*python" %i | cut -d: -f1`
