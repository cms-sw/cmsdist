### RPM external cgal 4.2

Source: https://gforge.inria.fr/frs/download.php/32360/%{n}-%{realversion}.tar.bz2
Patch0: cgal-4.2-cmake-string-replace

BuildRequires: cmake
Requires: gmp-static mpfr-static

Requires: boost zlib

%define drop_files %{i}/{share,bin} %{i}/lib/CGAL

%prep
%setup -n CGAL-%{realversion}
%patch0 -p1

%build

export MPFR_LIB_DIR="${MPFR_STATIC_ROOT}/lib"
export MPFR_INC_DIR="${MPFR_STATIC_ROOT}/include"
export GMP_LIB_DIR="${GMP_STATIC_ROOT}/lib"
export GMP_INC_DIR="${GMP_STATIC_ROOT}/include"

cmake . \
  -DCMAKE_INSTALL_PREFIX:PATH="%{i}" \
  -DCMAKE_SKIP_RPATH:BOOL=YES \
  -DWITH_BLAS:BOOL=OFF \
  -DWITH_CGAL_Core:BOOL=ON \
  -DWITH_CGAL_ImageIO:BOOL=ON \
  -DWITH_CGAL_Qt3:BOOL=OFF \
  -DWITH_CGAL_Qt4:BOOL=OFF \
  -DWITH_Coin3D:BOOL=OFF \
  -DWITH_ESBTL:BOOL=OFF \
  -DWITH_Eigen3:BOOL=OFF \
  -DWITH_GMP:BOOL=ON \
  -DWITH_GMPXX:BOOL=OFF \
  -DWITH_IPE:BOOL=OFF \
  -DWITH_LAPACK:BOOL=OFF \
  -DWITH_LEDA:BOOL=OFF \
  -DWITH_MPFI:BOOL=OFF \
  -DWITH_MPFR:BOOL=ON \
  -DWITH_NTL:BOOL=OFF \
  -DWITH_OpenGL:BOOL=OFF \
  -DWITH_OpenNL:BOOL=OFF \
  -DWITH_QGLViewer:BOOL=OFF \
  -DWITH_RS:BOOL=OFF \
  -DWITH_RS3:BOOL=OFF \
  -DWITH_TAUCS:BOOL=OFF \
  -DWITH_ZLIB:BOOL=ON \
  -DWITH_demos:BOOL=OFF \
  -DWITH_examples:BOOL=OFF \
  -DZLIB_ROOT="${ZLIB_ROOT}" \
  -DCGAL_ENABLE_PRECONFIG:BOOL=NO \
  -DCGAL_IGNORE_PRECONFIGURED_GMP:BOOL=YES \
  -DCGAL_IGNORE_PRECONFIGURED_MPFR:BOOL=YES \
  -DBoost_NO_SYSTEM_PATHS:BOOL=TRUE \
  -DBOOST_ROOT:PATH="${BOOST_ROOT}"

make VERBOSE=1

%install
make install VERBOSE=1
# bla bla
