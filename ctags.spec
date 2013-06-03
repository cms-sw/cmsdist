### RPM external ctags 5.5.4
Source: http://surfnet.dl.sourceforge.net/sourceforge/ctags/ctags-%{v}.tar.gz

%build
./configure --prefix=%i
make 

%install
make install
