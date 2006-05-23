### RPM external glimpse 4.18.5
Source: http://webglimpse.net/trial/glimpse-%{v}.tar.gz

%prep
%setup -n glimpse-%v
%build
./configure --prefix=%{i} 
make 

%install
make install
