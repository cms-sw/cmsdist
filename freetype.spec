### RPM external freetype 2.3.0
Source: http://www.very-clever.com/download/nongnu/freetype/freetype-%{v}.tar.gz
%prep
%setup -n freetype-%{v}
%build
./configure --prefix=%i
make %makeprocesses

%install
make install
mkdir -p %i/etc/profile.d

%post
%files
%i/

