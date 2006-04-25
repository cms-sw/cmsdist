### RPM external libjpg 6b
Source: ftp://ftp.uu.net/graphics/jpeg/jpegsrc.v%{v}.tar.gz
%prep
%setup -n jpeg-%v
%build
./configure --prefix=%{i} --enable-shared
make LIBTOOL=$(which libtool) %makeprocesses
