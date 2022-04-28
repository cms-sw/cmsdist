### RPM external xpmem v2.6.3-20220308
%define commit 61c39efdea943ac863037d7e35b236145904e64d

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
