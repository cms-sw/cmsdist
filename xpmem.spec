### RPM external xpmem v2.6.3-20260218
%define commit 8ef21a81de33397352c9d8973b0d3102c84c139a

BuildRequires: autotools
Source: https://github.com/hjelmn/%{n}/archive/%{commit}.tar.gz

%prep
%setup -n %{n}-%{commit}

./autogen.sh
./configure \
  --prefix=%{i} \
  --enable-shared \
  --disable-static \
  --disable-dependency-tracking \
  --disable-kernel-module \
  --with-pic \
  --with-gnu-ld

%build
make %{makeprocesses}

%install
make install

# remove kernel module rules
rm -rf %{i}/etc

# remove the libtool library files
rm -f %{i}/lib/lib*.la

# remove pkg-config to avoid rpm-generated dependency on /usr/bin/pkg-config
rm -rf %{i}/lib/pkgconfig

%post
