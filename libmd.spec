### RPM external libmd 1.0.4
Source: https://archive.hadrons.org/software/%{n}/%{n}-%{realversion}.tar.xz

BuildRequires: autotools

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

./configure --prefix=%{i}
make %{makeprocesses}

%install
make install
