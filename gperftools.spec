### RPM external gperftools 2.6.1
Source: https://github.com/gperftools/gperftools/archive/gperftools-%{realversion}.tar.gz

BuildRequires: autotools

Requires: libunwind

%prep
%setup -n %{n}-%{n}-%{realversion}

%build
./autogen.sh
./configure \
  --prefix=%{i} \
  --disable-dependency-tracking \
  --enable-sized-delete \
  --enable-dynamic-sized-delete-support \
  --enable-libunwind \
  --disable-debugalloc \
  CPPFLAGS="-I${LIBUNWIND_ROOT}/include" \
  LDFLAGS="-L${LIBUNWIND_ROOT}/lib -L${LIBUNWIND_ROOT}/lib64"

make %{makeprocesses}

%install

make install

rm -rf %{i}/share/{doc,man}
# bla bla
