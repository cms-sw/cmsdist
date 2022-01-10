### RPM external rust 1.57.0
## NOCOMPILER

Provides: libc.so.6(GLIBC_2.2.5)(64bit)
%ifarch x86_64
Source: https://static.rust-lang.org/dist/rust-%{realversion}-x86_64-unknown-linux-gnu.tar.gz
%endif
%ifarch ppc64le
Provides: libc.so.6(GLIBC_2.2.5)(64bit)
Source: https://static.rust-lang.org/dist/rust-%{realversion}-powerpc64-unknown-linux-gnu.tar.gz
%endif
%ifarch aarch64
Source: https://static.rust-lang.org/dist/rust-%{realversion}-aarch64-unknown-linux-gnu.tar.gz
%endif

Provides: /bin/rc

%prep
%setup -n rust

%build

%install
./install.sh --prefix=%i --disable-ldconfig --disable-verify --without-rust-docs --without-llvm-tools-preview --without-cargo
# Drop documentation
rm -rf %i/{man,doc}