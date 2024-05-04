### RPM external rust 1.78.0
%ifarch ppc64le
%define build_arch powerpc64le-unknown-linux-gnu
%else
%define build_arch %{_arch}-unknown-linux-gnu
%endif
Source: https://static.rust-lang.org/dist/%{n}-%{realversion}-%{build_arch}.tar.gz
Requires: zlib
Provides: libLLVM.so.18.1-rust-1.78.0-stable()(64bit) libLLVM.so.18.1-rust-1.78.0-stable(LLVM_18.1)(64bit)

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
