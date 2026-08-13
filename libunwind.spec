### RPM external libunwind 1.8.3

Source0: https://github.com/%{n}/%{n}/archive/refs/tags/v%{realversion}.tar.gz
Source1: https://patch-diff.githubusercontent.com/raw/libunwind/libunwind/pull/831.patch

BuildRequires: autotools gmake
Requires: zlib xz

%prep
%setup -n %{n}-%{realversion}
patch -p1 <%{_sourcedir}/831.patch

%build
autoreconf -fiv
./configure CFLAGS="-g -O3 -fcommon" \
  CPPFLAGS="-I${ZLIB_ROOT}/include -I${XZ_ROOT}/include" \
  LDFLAGS="-L${ZLIB_ROOT}/lib -L${XZ_ROOT}/lib" \
  --disable-tests \
  --prefix=%{i} --disable-block-signals --enable-zlibdebuginfo --disable-per-thread-cache
make %{makeprocesses}

%install

make %{makeprocesses} install
[ -d %{i}/lib64 ] && mv %{i}/lib64 %{i}/lib
%define drop_files %{i}/share/man %{i}/lib/pkgconfig %{i}/lib/*.a
