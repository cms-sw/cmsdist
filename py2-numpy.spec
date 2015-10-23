### RPM external py2-numpy 1.10.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: http://downloads.sourceforge.net/project/numpy/NumPy/%realversion/numpy-%realversion.tar.gz
Requires: python zlib lapack

%prep
%setup -n numpy-%realversion

%build
%install
case %cmsos in
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac

export LAPACK_ROOT
export LAPACK=$LAPACK_ROOT/lib/liblapack.$SONAME
export BLAS=$LAPACK_ROOT/lib/libblas.$SONAME

python setup.py build --fcompiler=gnu95
python setup.py install --prefix=%i
#find %i -name '*.egg-info' -exec rm {} \;
