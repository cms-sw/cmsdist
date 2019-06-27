### RPM external sloccount 2.26
Source: http://www.dwheeler.com/sloccount/sloccount-%{realversion}.tar.gz

BuildRequires: flex

%prep
%setup -n sloccount-%{realversion}
%build
cp makefile makefile.dist
perl -p -i -e "s|^PREFIX=/usr/local|PREFIX=%i|g" makefile
make 

%install

mkdir -p %{i}/bin
make install

%post
# bla bla
