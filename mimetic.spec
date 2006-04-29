### RPM external mimetic 0.8.9
Source: http://codesink.org/download/%{n}-%{v}.tar.gz

%description

%build
./configure --prefix=%i
make

%install
make install



%changelog
* Mon Feb 27 2006 Stefano Argiro <argiro@pccms211.cern.ch> 
- Initial build.


