### RPM external glimpse 4.18.5
Source: http://webglimpse.net/trial/glimpse-%{realversion}.tar.gz

%prep
%setup -n glimpse-%realversion
%build
./configure --prefix=%{i} 
# Turn off this part, it causes problems for 32-bit-on-64-bit and is only
# needed for webglimpse
perl -p -i -e "s|dynfilters||g" Makefile
make 

%install
make install
