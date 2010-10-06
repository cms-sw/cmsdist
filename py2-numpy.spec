### RPM external py2-numpy 1.3.0
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
%define downloadn numpy
Source: http://switch.dl.sourceforge.net/sourceforge/%downloadn/%downloadn-%realversion.tar.gz
Patch0: py2-numpy-1.3.0

Requires: zlib python

%prep
%setup -n %downloadn-%realversion
%patch0 -p0

%build
python setup.py build

%install
export LAPACK_SRC=%_builddir/%downloadn-%realversion/LAPACK
export BLAS_SRC=%_builddir/%downloadn-%realversion/BLAS
python setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;
