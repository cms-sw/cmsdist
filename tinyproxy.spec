### RPM external tinyproxy 1.6.3
Source: dl.sourceforge.net/%n/%{n}-%{v}.tar.gz
%description

%build
./configure --prefix=%i
make

%install
make install



%changelog
* Mon Feb 27 2006 Stefano Argiro <argiro@pccms211.cern.ch> 
- Initial build.


