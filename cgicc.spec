### RPM external cgicc 3.2.3

Source: ftp://ftp.cgicc.org/%{n}-%{v}.tar.gz


%build
./configure --prefix=%i
make %makeprocesses

%install
make install



%changelog
* Mon Feb 27 2006 Stefano Argiro <argiro@pccms211.cern.ch> 
- Initial build.


