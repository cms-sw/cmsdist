### RPM external millepede V04-11-01
%define tag 4f288098f84f274f5a241f921035af77bc07d5c8
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
