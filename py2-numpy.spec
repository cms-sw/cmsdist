### RPM external py2-numpy 1.9.2
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
Source: http://downloads.sourceforge.net/project/numpy/NumPy/%{realversion}/numpy-%{realversion}.tar.gz
Requires: python
Requires: zlib
Requires: lapack
%prep
%setup -n numpy-%{realversion}

%build
%install
cat > site.cfg <<EOF
[DEFAULT]
libraries = lapack,blas
include_dirs = $LAPACK_ROOT/include
library_dirs = $LAPACK_ROOT/lib
EOF

python setup.py build --fcompiler=gnu95
python setup.py install --prefix=%{i}
find %{i} -name '*.egg-info' -exec rm {} \;
