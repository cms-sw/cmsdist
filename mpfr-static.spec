### RPM external mpfr-static 3.1.3

Source: http://www.mpfr.org/mpfr-%{realversion}/mpfr-%{realversion}.tar.bz2

BuildRequires: gmp-static

%define keep_archives true
%define drop_files %{i}/share

%prep
%setup -n mpfr-%{realversion}

%build
./configure \
  --enable-static \
  --disable-shared \
  --prefix=%{i} \
  --with-gmp=${GMP_STATIC_ROOT} \
  --with-pic \

make %{makeprocesses}

%install

make install
find %{i}/lib -name '*.la' -delete
# bla bla
