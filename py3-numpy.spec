### RPM external py3-numpy 1.13.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
#Source: http://downloads.sourceforge.net/project/numpy/NumPy/%realversion/numpy-%realversion.tar.gz
#Source: https://pypi.python.org/packages/e0/4c/515d7c4ac424ff38cc919f7099bf293dd064ba9a600e1e3835b3edefdb18/numpy-1.11.1.tar.gz
#Source: https://pypi.python.org/packages/b7/9d/8209e555ea5eb8209855b6c9e60ea80119dab5eff5564330b35aa5dc4b2c/numpy-1.12.0.zip
Source: https://pypi.python.org/packages/c0/3a/40967d9f5675fbb097ffec170f59c2ba19fc96373e73ad47c2cae9a30aed/numpy-1.13.1.zip
Requires: python3 py3-setuptools zlib lapack atlas

%prep
%setup -n numpy-%realversion

%build
%install
case %cmsos in
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac

export GCC_ROOT
export PYTHON3_ROOT
export ATLAS_ROOT
export ATLAS=$ATLAS_ROOT
export ZLIB_ROOT
export LAPACK_ROOT
export LAPACK=$LAPACK_ROOT/lib/liblapack.$SONAME
export BLAS=$LAPACK_ROOT/lib/libblas.$SONAME
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
export LD_LIBRARY_PATH=$PYTHON3_ROOT/lib:$LD_LIBRARY_PATH
python3 setup.py build --fcompiler=gnu95
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH python3 setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

# replace all instances of #!/path/bin/python into proper format
%py3PathRelocation

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
%addDependency

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
