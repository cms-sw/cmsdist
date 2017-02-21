### RPM external bison 3.0.4
Source: http://ftp.gnu.org/gnu/%{n}/%{n}-%{realversion}.tar.gz

BuildRequires: autotools

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
