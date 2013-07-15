### RPM external CGAL 4.2

Source: https://gforge.inria.fr/frs/download.php/32361/%{n}-%{realversion}.tar.xz

BuildRequires: cmake

Requires: boost gcc zlib

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++11
%endif

%define drop_files %{i}/{share,bin} %{i}/lib/CGAL

%prep
%setup -n %{n}-%{realversion}

%build

SOLIB_EXT=so
case "%{cmsplatf}" in
  osx*)
    SOLIB_EXT=dylib
    ;;
esac

export MPFR_LIB_DIR="${GCC_ROOT}/lib"
export MPFR_INC_DIR="${GCC_ROOT}/include"
export GMP_LIB_DIR="${GCC_ROOT}/lib"
export GMP_INC_DIR="${GCC_ROOT}/include"

cmake . \
  -DCMAKE_CXX_COMPILER:STRING="%{cms_cxx}" \
  -DCMAKE_CXX_FLAGS:STRING="%{cms_cxxflags} -I${GCC_ROOT}/include" \
  -DCMAKE_SHARED_LINKER_FLAGS:STRING="-L${GCC_ROOT}/lib" \
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
  -DZLIB_INCLUDE_DIR:PATH="${ZLIB_ROOT}/include" \
  -DZLIB_LIBRARY:FILEPATH="${ZLIB_ROOT}/lib/libz.${SOLIB_EXT}" \
  -DCGAL_ENABLE_PRECONFIG:BOOL=NO \
  -DCGAL_IGNORE_PRECONFIGURED_GMP:BOOL=YES \
  -DCGAL_IGNORE_PRECONFIGURED_MPFR:BOOL=YES \
  -DBoost_NO_SYSTEM_PATHS:BOOL=TRUE \
  -DBOOST_ROOT:PATH="${BOOST_ROOT}"

make VERBOSE=1

%install
make install VERBOSE=1
