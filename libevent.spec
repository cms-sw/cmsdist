### RPM external libevent 2.0.22
Source: http://sourceforge.net/projects/levent/files/libevent/libevent-2.0/libevent-%{realversion}-stable.tar.gz
%prep 
%setup -n libevent-%realversion-stable

%build
./configure --prefix=%i
make

%install
make install


