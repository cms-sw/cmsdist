### RPM external sloccount 2.26
Source: http://www.dwheeler.com/sloccount/sloccount-%{v}.tar.gz

%prep
%setup -n sloccount-%v
%build
cp makefile makefile.dist
perl -p -i -e "s|^PREFIX=/usr/local|PREFIX=%i|g" makefile
make 

%install

mkdir -p %{i}/bin
make install

%post
