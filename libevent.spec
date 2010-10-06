### RPM external libevent 1.4.9
Source: http://www.monkey.org/~provos/libevent-%{realversion}-stable.tar.gz

%prep 
%setup -n libevent-%realversion-stable

%build
./configure --prefix=%i
make

%install
make install


