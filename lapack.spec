### RPM external lapack 3.0.2
# NB: based on http://www.netlib.org/lapack/rpms
Source0: http://www.netlib.org/lapack/lapack.tgz
Source1: http://www.netlib.org/lapack/manpages.tgz
Source2: lapack-makefile-blas
Source3: lapack-makefile-lapack

%prep
%setup -q -n LAPACK
%setup -q -D -T -a 1 -n LAPACK
cp %{_sourcedir}/lapack-makefile-blas BLAS/SRC/Makefile
cp %{_sourcedir}/lapack-makefile-lapack SRC/Makefile

%build
cd BLAS/SRC
FFLAGS="$RPM_OPT_FLAGS" make static
cp libblas.a ../..
make clean
FFLAGS="$RPM_OPT_FLAGS -fPIC" make static shared
cp libblas.a ../../libblas_pic.a
cp libblas.so.2.0.1 ../..
cd ../..
ln -s libblas.so.2.0.1 libblas.so
cd SRC
FFLAGS="$RPM_OPT_FLAGS" make static
cp liblapack.a ..
make clean
FFLAGS="$RPM_OPT_FLAGS -fPIC" make static shared
cp liblapack.a ../liblapack_pic.a
cp liblapack.so.2.0.1 ..   

%install
mkdir -p %i/lib
cp -f lib*.so* lib*.a %i/lib

cd %i/lib
ln -sf liblapack.so.2.0.1 liblapack.so
ln -sf liblapack.so.2.0.1 liblapack.so.2
ln -sf liblapack.so.2.0.1 liblapack.so.2.0
ln -sf libblas.so.2.0.1 libblas.so
ln -sf libblas.so.2.0.1 libblas.so.2
ln -sf libblas.so.2.0.1 libblas.so.2.0
