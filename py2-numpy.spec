### RPM external py2-numpy 1.5.1
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
%define downloadn numpy
Source: http://switch.dl.sourceforge.net/sourceforge/%downloadn/%downloadn-%realversion.tar.gz
Patch0: py2-numpy-1.5.1-fix-macosx-build

Requires: python
Requires: zlib
Requires: lapack
%prep
%setup -n %downloadn-%realversion
case %cmsos in
  osx*)
%patch0 -p1
  ;;
esac

%build
%install
case %cmsos in 
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac

LAPACK=$LAPACK_ROOT/lib/liblapack.$SONAME
BLAS=$LAPACK_ROOT/lib/libblas.$SONAME

LAPACK=$LAPACK BLAS=$BLAS python setup.py build --fcompiler "`which gfortran`"
LAPACK=$LAPACK BLAS=$BLAS python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
