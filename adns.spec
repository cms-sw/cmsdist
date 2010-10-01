### RPM external adns 1.4
Source: http://www.chiark.greenend.org.uk/~ian/adns/ftp/adns-%realversion.tar.gz

%prep
%setup -n %n-%realversion

%build
./configure --prefix=%i
make %makeprocesses

%install
make install
