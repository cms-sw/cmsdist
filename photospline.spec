### RPM external photospline 1301.2184v1
Source0: http://arxiv.org/e-print/%{realversion}
BuildRequires: cmake suitesparse
Requires: fitsio gsl python lapack python py2-numpy

%prep
tar xzvf %{_sourcedir}/%{realversion}
%build
%install
cd photospline
rm -rf CMakeFiles CMakeCache.txt
mkdir -p build
cd build
export SUITESPARSEROOT=$SUITESPARSE_ROOT
cmake  -DCMAKE_INSTALL_PREFIX=%i -DCFITSIO_LIBRARIES=$FITSIO_ROOT/lib/libcfitsio.a \
       -DCFITSIO_INCLUDE_DIR=$FITSIO_ROOT/include \
       -DGSL_LIBRARY_DIR=$GSL_ROOT/lib \
       -DGSL_INCLUDE_DIR=$GSL_ROOT/include \
       -DBLAS_LIBRARIES=${LAPACK_ROOT}/lib/libblas.so \
       -DLAPACK_LIBRARIES=${LAPACK_ROOT}/lib/liblapack.so \
       -DPYTHON_LIBRARY=$PYTHON_ROOT/lib/libpython2.7.so \
       -DPYTHON_INCLUDE_DIR=$PYTHON_ROOT/include/python2.7 \
       -DSUITESPARSE_INCLUDE_DIR=$SUITESPARSE_ROOT/include \
       ..
make %{makeprocesses} ; make install
# bla bla
