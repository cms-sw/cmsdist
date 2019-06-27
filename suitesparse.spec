### RPM external suitesparse 4.2.1

Source0: http://www.cise.ufl.edu/research/sparse/SuiteSparse/SuiteSparse-%realversion.tar.gz
Requires: lapack
%define keep_archives true

%prep
%setup -n SuiteSparse
%build
make -j %makeprocesses LAPACK="-L$LAPACK_ROOT/lib -llapack" BLAS="-L$LAPACK_ROOT/lib -lblas"
%install
mkdir -p %i/{lib,include}
make install INSTALL_LIB="%i/lib" INSTALL_INCLUDE="%i/include"
# bla bla
