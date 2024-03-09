### RPM external millepede V04-16-00
Source: https://gitlab.desy.de/claus.kleinwort/millepede-ii/-/archive/%{realversion}/%{n}-ii-%{realversion}.tar.gz
Requires: zlib

%prep
%setup -n %{n}-ii-%{realversion}

%build
make \
  ZLIB_INCLUDES_DIR="${ZLIB_ROOT}/include" \
  ZLIB_LIBS_DIR="${ZLIB_ROOT}/lib"

%install
make install PREFIX=%{i}
