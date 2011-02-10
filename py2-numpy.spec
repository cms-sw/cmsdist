### RPM external py2-numpy 1.5.1
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
%define downloadn numpy
Source: http://switch.dl.sourceforge.net/sourceforge/%downloadn/%downloadn-%realversion.tar.gz

Requires: python
Requires: zlib
Requires: lapack
%prep
%setup -n %downloadn-%realversion

%build
%install
export LAPACK_SRC=%_builddir/%downloadn-%realversion/LAPACK
export BLAS_SRC=%_builddir/%downloadn-%realversion/BLAS

python setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/py2-numpy.xml
<tool name="py2-numpy" version="%v">
<client>
<environment name="PY2NUMPY_BASE" default="%i"/>
</client>
<runtime name="PYTHONPATH" value="$PY2NUMPY_BASE/lib/python2.6/site-packages" type="path"/>
</tool>
EOF_TOOLFILE
