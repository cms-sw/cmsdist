### RPM external py2-numpy 1.6.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: http://downloads.sourceforge.net/project/numpy/NumPy/%realversion/numpy-%realversion.tar.gz
Patch0: py2-numpy-%realversion-fix-macosx-build

Requires: python
Requires: zlib
Requires: lapack
%prep
%setup -n numpy-%realversion
%ifos darwin
%patch0 -p1
%endif

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
find %i -name '*.egg-info' -exec rm {} \;
