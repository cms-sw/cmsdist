### RPM external libjpg 6b
Source: ftp://ftp.uu.net/graphics/jpeg/jpegsrc.v%{v}.tar.gz
%prep
%setup -n jpeg-%v
%build
./configure --prefix=%{i} --enable-shared
make %makeprocesses
%install
mkdir -p %{i}/lib
mkdir -p %{i}/bin
mkdir -p %{i}/include
mkdir -p %{i}/man/man1
make install
