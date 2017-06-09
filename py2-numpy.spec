### RPM external py2-numpy 1.6.1
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
Source: http://downloads.sourceforge.net/project/numpy/NumPy/%{realversion}/numpy-%{realversion}.tar.gz
Patch0: py2-numpy-%{realversion}-fix-macosx-build

%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)

Requires: python
Requires: zlib
Requires: lapack
%prep
%setup -n numpy-%{realversion}
%if %isdarwin
%patch0 -p1
%endif

%build
%install
case %{cmsos} in 
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac

cat > site.cfg <<EOF
[blas]
include_dirs = $LAPACK_ROOT/include
library_dirs = $LAPACK_ROOT/lib64
blas_libs = blas
[lapack]
include_dirs = $LAPACK_ROOT/include
library_dirs = $LAPACK_ROOT/lib64
lapack_libs = lapack
EOF

export ATLAS=None
export OPENBLAS=None


python setup.py build  --fcompiler=gnu95
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH python setup.py install --prefix=%i

find %{i} -name '*.egg-info' -exec rm {} \;
