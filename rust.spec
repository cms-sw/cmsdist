### RPM external rust 1.57.0
## NOCOMPILER

%ifarch x86_64
Source: https://static.rust-lang.org/dist/rust-%{realversion}-x86_64-unknown-linux-gnu.tar.gz
%endif
%ifarch ppc64le
Source: https://static.rust-lang.org/dist/rust-%{realversion}-powerpc64-unknown-linux-gnu.tar.gz
%endif
%ifarch aarch64
Source: https://static.rust-lang.org/dist/rust-%{realversion}-aarch64-unknown-linux-gnu.tar.gz
%endif

Provides: /bin/rc

%prep
%ifarch x86_64
%setup -n rust-%{realversion}-x86_64-unknown-linux-gnu
%endif
%ifarch ppc64le
%setup -n rust-%{realversion}-powerpc64-unknown-linux-gnu
%endif
%ifarch aarch64
%setup -n rust-%{realversion}-aarch64-unknown-linux-gnu
%endif

%build

%install
./install.sh --prefix=%i --disable-ldconfig --disable-verify
# Drop documentation
rm -rf %i/share/{man,doc}