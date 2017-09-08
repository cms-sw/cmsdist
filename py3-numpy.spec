### RPM external py3-numpy 1.12.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
#Source: http://downloads.sourceforge.net/project/numpy/NumPy/%realversion/numpy-%realversion.tar.gz
#Source: https://pypi.python.org/packages/e0/4c/515d7c4ac424ff38cc919f7099bf293dd064ba9a600e1e3835b3edefdb18/numpy-1.11.1.tar.gz
Source: https://pypi.python.org/packages/b7/9d/8209e555ea5eb8209855b6c9e60ea80119dab5eff5564330b35aa5dc4b2c/numpy-1.12.0.zip
Requires: python3 py3-setuptools zlib lapack atlas

%prep
%setup -n numpy-%realversion

%build
%install
case %cmsos in
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac

export ATLAS_ROOT
export LAPACK_ROOT
export LAPACK=$LAPACK_ROOT/lib/liblapack.$SONAME
export BLAS=$LAPACK_ROOT/lib/libblas.$SONAME
#export A1=$ATLAS_ROOT/lib/libatlas.a
#export A2=$ATLAS_ROOT/lib/libcblas.a
#export A3=$ATLAS_ROOT/lib/libf77blas.a
#export A4=$ATLAS_ROOT/lib/liblapack.a
#export A5=$ATLAS_ROOT/lib/libptcblas.a
#export A5=$ATLAS_ROOT/lib/libptf77blas.a
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES

#export GCC_ROOT
#export MAIN="$GCC_ROOT/lib64/libcilkrts.so"
export PYTHON3_ROOT
#LDFLAGS="-L$PYTHON3_ROOT/lib $LDFLAGS -L$ATLAS_ROOT/lib -latlas  -lcblas -lf77blas -llapack -lptcblas -lptf77blas" \
#LDFLAGS="-L$PYTHON3_ROOT/lib $LDFLAGS $LAPACK $BLAS -L$ATLAS_ROOT -latlas  -lcblas -lf77blas -llapack -lptcblas -lptf77blas" \
#LDFLAGS="-L$PYTHON3_ROOT/lib $LDFLAGS $LAPACK $BLAS $A1 $A2 $A3 $A4 $A5 $A6" \
#LDFLAGS="-L$PYTHON3_ROOT/lib -L$GCC_ROOT/lib64 $LDFLAGS $LAPACK $BLAS $MAIN" \
#LDFLAGS="-L$PYTHON3_ROOT/lib $LDFLAGS $LAPACK $BLAS" \
#LDFLAGS="-L$PYTHON3_ROOT/lib $LDFLAGS" \
echo "PYTHON_LIB=${PYTHON_LIB_SITE_PACKAGES}"
echo "PYTHON3_ROOT=$PYTHON3_ROOT"
$PYTHON3_ROOT/bin/python3 setup.py build --fcompiler=gnu95
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH $PYTHON3_ROOT/bin/python3 setup.py install --prefix=%i
#find %i -name '*.egg-info' -exec rm {} \;

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
