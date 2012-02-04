### RPM external py2-matplotlib 1.0.1
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
Source: http://sourceforge.net/projects/matplotlib/files/matplotlib/matplotlib-%{realversion}/matplotlib-%{realversion}.tar.gz

Requires: py2-numpy 
Requires: zlib
Requires: libpng
%prep
%setup -n matplotlib-%{realversion}

cat >> setup.cfg <<- EOF
[build_ext]
include_dirs = $LIBPNG_ROOT/include:$ZLIB_ROOT/include:/usr/X11R6/include:/usr/X11R6/include/freetype2
library_dirs = $LIBPNG_ROOT/lib:$ZLIB_ROOT/lib:/usr/X11/lib
EOF

%build
# Pick up the system compiler also when building with gcc 4.6.1 on mac.
case %cmsos in 
  osx*_*_gcc421) ;;
  osx*) 
    export PATH=/Developer/usr/bin:$PATH
    export CC='/Developer/usr/bin/llvm-gcc-4.2'
    export CXX='/Developer/usr/bin/llvm-g++-4.2'
  ;;
esac
python setup.py build 

%install
python -c 'import numpy'
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

# No need for test files
rm -rf %i/$PYTHON_LIB_SITE_PACKAGES/matplotlib/tests
