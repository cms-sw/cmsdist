### RPM external gmp 4.1.4

Source: http://ftp.sunet.se/pub/gnu/gmp/%{n}-%{v}.tar.gz


%build
./configure --prefix=%i
make

%install
make install



%changelog
* Mon Feb 27 2006 Stefano Argiro <argiro@pccms211.cern.ch> 
- Initial build.


