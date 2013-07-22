### RPM external bison 2.7.1
Source: http://ftp.gnu.org/gnu/%{n}/%{n}-%{realversion}.tar.gz

%define drop_files %{i}/share/{man,locale,info}

%prep
%setup -q -n %{n}-%{realversion}

%build
./configure \
  --build=%{_build} \
  --host="%{_host}" \
  --prefix=%{i} \
  --disable-nls \
  --disable-rpath \
  --enable-dependency-tracking

make %{makeprocesses}

%install
make install
