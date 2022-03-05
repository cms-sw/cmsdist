### RPM external millepede V04-11-01
%define tag 9ee817fc61fe3e1b6543a8a16f7bcd8e1f8c331f
Source: git+https://gitlab.desy.de/claus.kleinwort/millepede-ii.git?obj=main/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Requires: zlib

%prep
%setup -n %{n}-%{realversion}

%build
make \
  ZLIB_INCLUDES_DIR="${ZLIB_ROOT}/include" \
  ZLIB_LIBS_DIR="${ZLIB_ROOT}/lib"

%install
make install PREFIX=%{i}
