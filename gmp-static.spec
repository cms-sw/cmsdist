### RPM external gmp-static 6.2.0

Source: https://ftp.gnu.org/gnu/gmp/gmp-%realversion.tar.xz

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
