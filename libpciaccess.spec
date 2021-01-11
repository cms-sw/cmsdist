### RPM external libpciaccess 0.16
# use the packaged sources from Debian instead of the developer sources from Xorg gitlab
# to avoid the dependency on the xorg-macros package
Source: http://deb.debian.org/debian/pool/main/libp/%{n}/%{n}_%{realversion}.orig.tar.gz

BuildRequires: autotools
Requires: zlib

%prep
%setup -n %{n}-%{realversion}

%build
./configure \
  --prefix %{i} \
  --disable-dependency-tracking \
  --enable-shared \
  --disable-static \
  --with-pic \
  --with-gnu-ld \
  --with-zlib \
  CPPFLAGS="-I$ZLIB_ROOT/include" \
  LDFLAGS="-L$ZLIB_ROOT/lib"

%post
