### RPM external py2-numpy 1.9.2
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
Source: http://downloads.sourceforge.net/project/numpy/NumPy/%{realversion}/numpy-%{realversion}.tar.gz
Requires: python
Requires: zlib
Requires: atlas
%prep
%setup -n numpy-%{realversion}

%build
%install
case %{cmsos} in 
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac

cat > site.cfg <<EOF
[atlas]
libraries = lapack,f77blas,cblas,atlas
include_dirs = $ATLAS_ROOT/include
library_dirs = $ATLAS_ROOT/lib
EOF

python setup.py build --fcompiler=gnu95
python setup.py install --prefix=%{i}
find %{i} -name '*.egg-info' -exec rm {} \;
