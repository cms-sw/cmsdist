### RPM external py2-matplotlib 0.87.4
## INITENV +PATH PYTHONPATH %i/lib/python$(echo $PYTHON_VERSION | cut -d. -f 1,2)/site-packages
%define downloadn matplotlib
Source: http://switch.dl.sourceforge.net/sourceforge/%downloadn/%downloadn-%v.tar.gz
Patch: py2-matplotlib.patch
Requires: python
# Requires: zlib
# Requires: agg
# Requires: cairo
Requires: py2-numarray
Requires: libpng
# Requires: freetype
%prep
%setup -n %downloadn-%v
%patch
pythonv=$(echo $PYTHON_VERSION | cut -d. -f 1,2)
perl -p -i -e "s,numarray_inc_dirs =.*,numarray_inc_dirs = ['$PY2_NUMARRAY_ROOT/include/python$pythonv']," setupext.py

%build
%install
python setup.py install --prefix=%i
perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" `grep -r -e "#\!.*python" %i | cut -d: -f1`
