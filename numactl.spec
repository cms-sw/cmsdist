### RPM external numactl 2.0.14
## INITENV +PATH MANPATH %i/share/man
BuildRequires: autotools
Source: https://github.com/%{n}/%{n}/archive/v%{realversion}.tar.gz

%prep
%setup -n %{n}-%{realversion}

./autogen.sh
./configure \
  --prefix=%{i} \
  --enable-shared \
  --disable-static \
  --disable-dependency-tracking \
  --with-pic \
  --with-gnu-ld

%build
make %{makeprocesses}

%install
make install

# Remove pkg-config to avoid rpm-generated dependency on /usr/bin/pkg-config
rm -rf %{i}/lib/pkgconfig

%post
