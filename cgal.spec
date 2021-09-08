### RPM external cgal 5.3

Source: https://github.com/CGAL/cgal/releases/download/v%{realversion}/CGAL-%{realversion}.tar.xz

BuildRequires: cmake
Requires: gmp-static mpfr-static

Requires: boost zlib

%define drop_files %{i}/{share,bin} %{i}/lib/CGAL

%prep
%setup -n CGAL-%{realversion}

%build

export MPFR_LIB_DIR="${MPFR_STATIC_ROOT}/lib"
export MPFR_INC_DIR="${MPFR_STATIC_ROOT}/include"
export GMP_LIB_DIR="${GMP_STATIC_ROOT}/lib"
export GMP_INC_DIR="${GMP_STATIC_ROOT}/include"

cmake . \
  -DCMAKE_INSTALL_PREFIX:PATH="%{i}" \
  -DWITH_demos:BOOL=OFF \
  -DWITH_examples:BOOL=OFF \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo

make VERBOSE=1

%install
make install VERBOSE=1
