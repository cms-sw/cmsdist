### RPM external gmp-static 6.1.0

Source: http://davidlt.web.cern.ch/davidlt/vault/gmp-%{realversion}.tar.bz2

BuildRequires: autotools

%define keep_archives true
%define drop_files %{i}/share

%prep
%setup -n gmp-%{realversion}

%build
./configure \
  --prefix=%{i} \
  --build=%{_build} \
  --host=%{_host} \
  --disable-shared \
  --enable-static \
  --enable-cxx \
  --with-pic

make %{makeprocesses}

%install

make install
find %{i}/lib -name '*.la' -delete
# bla bla
