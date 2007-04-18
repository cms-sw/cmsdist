### RPM external py2-numpy 1.0.1
Requires: gcc-wrapper
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
%define downloadn numpy
Source: http://switch.dl.sourceforge.net/sourceforge/%downloadn/%downloadn-%v.tar.gz
Patch0: py2-numpy-build 
Requires: python
Requires: zlib
%prep
%setup -n %downloadn-%v
%patch0 -p0
%build
## IMPORT gcc-wrapper
%install
export LAPACK_SRC=%_builddir/%downloadn-%v/LAPACK
export BLAS_SRC=%_builddir/%downloadn-%v/BLAS
env
python setup.py install --prefix=%i
perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" `grep -r -e "#\!.*python" %i | cut -d: -f1`
