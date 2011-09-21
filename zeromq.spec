### RPM external zeromq 2.1.9
Source: http://download.zeromq.org/%n-%realversion.tar.gz

%prep
%setup -n %n-%realversion

%build
./configure --prefix=%i
make %makeprocesses

%install
make install
