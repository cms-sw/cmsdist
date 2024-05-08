### RPM external rust 1.78.0
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

# set *.so permission so that rpmbuild can properly find the Provides
chmod 0755 %{i}/lib/*.so 
%ifarch x86_64
# files doesn't exist on ARM
chmod 0755 %{i}/lib/libLLVM*stable
%endif

#Remove doc/man
rm -rf %{i}/share
rm -f %{i}/lib/rustlib/install.log

%{relocateConfig}lib/rustlib/manifest-rust-std-x86_64-unknown-linux-gnu
%{relocateConfig}lib/rustlib/manifest-cargo
%{relocateConfig}lib/rustlib/manifest-rustc

