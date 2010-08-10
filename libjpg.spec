### RPM external libjpg 8b
Source: http://www.ijg.org/files/jpegsrc.v%{realversion}.tar.gz

%prep
%setup -n jpeg-%realversion

%build
./configure --prefix=%{i} --enable-shared --enable-static

make %makeprocesses
%install
mkdir -p %{i}/lib
mkdir -p %{i}/bin
mkdir -p %{i}/include
mkdir -p %{i}/man/man1
make install

%post
%{relocateConfig}lib/libjpeg.la
