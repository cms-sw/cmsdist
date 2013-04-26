### RPM external libevent 2.0.10
Source: http://www.monkey.org/~provos/libevent-%{realversion}-stable.tar.gz

%prep 
%setup -n libevent-%realversion-stable

%build
./configure --prefix=%i
make

%install
make install


