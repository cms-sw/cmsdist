### RPM external rust 1.69.0
%ifarch ppc64le
%define build_arch powerpc64le-unknown-linux-gnu
%else
%define build_arch %{_arch}-unknown-linux-gnu
%endif
Source: https://static.rust-lang.org/dist/%{n}-%{realversion}-%{build_arch}.tar.gz
Requires: zlib

%prep
%setup -n %{n}-%{realversion}-%{build_arch}

%build

%install
./install.sh --verbose --prefix=%{i} \
  --disable-ldconfig \
  --without=rust-docs \
  --components=rustc,cargo,rust-std-%{build_arch}

#set *.so permission so that rpmbuild can properly find the Provides
chmod 0755 %{i}/lib/*.so

#Remove doc/man
rm -rf %{i}/share
