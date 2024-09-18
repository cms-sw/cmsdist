### RPM external libpng 1.6.44
Source: https://github.com/pnggroup/libpng/archive/refs/tags/v%{realversion}.tar.gz

BuildRequires: autotools gmake
Requires: zlib

%prep
%setup -n %{n}-%{realversion}

%build
autoreconf -fiv

./configure \
  --prefix=%{i} \
  --disable-silent-rules \
  CPPFLAGS="-I${ZLIB_ROOT}/include" \
  LDFLAGS="-L${ZLIB_ROOT}/lib"

make %{makeprocesses}

%install
make install

# Strip libraries, we are not going to debug them.
%define strip_files %i/lib
%define drop_files %{i}/share

%post
%{relocateConfig}bin/libpng-config
%{relocateConfig}bin/libpng16-config
