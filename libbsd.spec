### RPM external libbsd 0.11.5
Source: https://libbsd.freedesktop.org/releases/%{n}-%{realversion}.tar.xz

BuildRequires: autotools
Requires: libmd

%define drop_files %{i}/share %{i}/lib/pkgconfig

%prep
%setup -n %{n}-%{realversion}

%build
autoreconf -i -f
# Update to detect aarch64 and ppc64le
rm -f ./build-aux/config.{sub,guess}
%get_config_sub ./build-aux/config.sub
%get_config_guess ./build-aux/config.guess
chmod +x ./build-aux/config.{sub,guess}

./configure --prefix=%{i} LDFLAGS="-L${LIBMD_ROOT}/lib" CFLAGS="-I${LIBMD_ROOT}/include"
make %{makeprocesses} LDFLAGS="-L${LIBMD_ROOT}/lib" CFLAGS="-I${LIBMD_ROOT}/include"

%install
make install

%post
%{relocateConfig}lib/libbsd.so
