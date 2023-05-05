### RPM external millepede V04-13-02
Source: https://gitlab.desy.de/claus.kleinwort/millepede-ii/-/archive/%{realversion}/%{n}-ii-%{realversion}.tar.gz
Requires: zlib OpenBLAS

%prep
%setup -n %{n}-ii-%{realversion}

%build
make \
  ZLIB_INCLUDES_DIR="${ZLIB_ROOT}/include" \
  ZLIB_LIBS_DIR="${ZLIB_ROOT}/lib" \
  SUPPORT_LAPACK64=yes \
  LAPACK64_LIBS_DIR="${OPENBLAS_ROOT}/lib" \
  LAPACK64_LIB=openblas

%install
make install PREFIX=%{i}
